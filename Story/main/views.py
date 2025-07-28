from django.shortcuts import render
from stories.models import Story
from contact.models import Contact

# View to render the homepage with the latest 3 stories and all user messages
def home_view(request):
    latest_stories = Story.objects.order_by('-created_at')[:3] 
    messages = Contact.objects.order_by('-created_at')
    return render(request, 'main/home.html', {
        'latest_stories': latest_stories,
        'messages': messages
    })

# View to render the About Us page
def about_view(request):
    return render(request, 'main/about.html')