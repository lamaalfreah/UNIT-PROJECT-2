from django.shortcuts import render, get_object_or_404, redirect
from .models import Story, Comment 
from .forms import StoryForm, CommentForm 
from django.db.models import Q
from django.conf import settings
import cohere
import edge_tts
import asyncio
from django.http import HttpResponse,HttpRequest
import re

# View to list all stories with optional filtering by topic and category
def all_stories_view(request:HttpRequest):
    stories = Story.objects.all()
    topic = request.GET.get('topic')
    category = request.GET.get('category')

    if topic:
        stories = stories.filter(topic__icontains=topic)
    if category:
        stories = stories.filter(category=category)

    stories = stories.order_by('-created_at')
    return render(request, 'stories/all_stories.html', {'stories': stories})

# View to add a new story, optionally generate content using AI (Cohere)
def add_story_view(request:HttpRequest):
    form = StoryForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if 'generate' in request.POST:
            print("AI GENERATE BUTTON CLICKED")
            if form.is_valid():
                # Extract data from form
                title = form.cleaned_data['title']
                child_name = form.cleaned_data['child_name']
                topic = form.cleaned_data['topic']
                category = form.cleaned_data['category']
                image = request.FILES.get('image') 
                
                # Generate story using Cohere
                co = cohere.Client(settings.COHERE_API_KEY)
                prompt = f"Write a children's story titled '{title}' for a child named {child_name}, based on the topic '{topic}' and category '{category}'. Make the story as rich and long as possible, using up to the maximum token limit."
                print("PROMPT:", prompt)
                response = co.generate(
                    model='command',
                    prompt=prompt,
                    max_tokens=400
                )
                print("COHERE RESPONSE:", response)
                generated_text = response.generations[0].text.strip()
                print("GENERATED TEXT:", generated_text)

                form = StoryForm(data={
                    'title': title,
                    'child_name': child_name,
                    'topic': topic,
                    'category': category,
                    'content': generated_text
                }, files={'image': image} if image else None) 
                return render(request, 'stories/add_story.html', {'form': form})

        elif 'submit' in request.POST:  # User clicked Save Story
            if form.is_valid():
                form.save()
                return redirect('stories:all_stories')

    return render(request, 'stories/add_story.html', {'form': form})

# View to display a specific story with comments and related stories
def story_detail_view(request:HttpRequest, story_id):
    story = get_object_or_404(Story, id=story_id)

    related_stories = Story.objects.filter(
        category=story.category
    ).exclude(id=story.id)[:3]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.save()
            return redirect('stories:story_detail', story_id=story.id)
    else:
        form = CommentForm()

    return render(request, 'stories/story_detail.html', {
        'story': story,
        'form': form,
        'related_stories': related_stories
    })

# View to update an existing story
def update_story_view(request:HttpRequest, story_id):
    story = get_object_or_404(Story, id=story_id)
    form = StoryForm(request.POST or None, request.FILES or None, instance=story)
    if form.is_valid():
        form.save()
        return redirect('stories:story_detail', story_id=story.id)
    return render(request, 'stories/update_story.html', {'form': form, 'story': story})

# View to delete a story 
def delete_story_view(request:HttpRequest, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == 'POST':
        story.delete()
        return redirect('stories:all_stories')
    return render(request, 'stories/delete_story.html', {'story': story})

# View to search stories by title, topic, or child's name
def search_stories_view(request:HttpRequest):
    query = request.GET.get('q')
    results = []
    if query:
        results = Story.objects.filter(
            Q(title__icontains=query) |
            Q(topic__icontains=query) |
            Q(child_name__icontains=query)
        )
    return render(request, 'stories/search_stories.html', {'results': results, 'query': query})

# Clean text by removing non-ASCII characters
def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text).strip()

# Convert story content to speech using Edge TTS and stream it as audio
def story_tts(request:HttpRequest, pk):
    story = Story.objects.get(pk=pk)
    text = story.content

    text = clean_text(story.content)
    print("TEXT TO READ:", text)

    if not text or len(text.strip()) < 10:
        return HttpResponse("The story content is too short or empty.", status=400)

    async def generate_audio():
        try:
            communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
            audio = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
            return audio
        except Exception as e:
            print("EDGE TTS ERROR:", str(e))
            return None

    audio_content = asyncio.run(generate_audio())

    if not audio_content:
        return HttpResponse("Failed to generate audio.", status=500)

    return HttpResponse(audio_content, content_type="audio/mpeg")