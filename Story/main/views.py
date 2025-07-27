from django.shortcuts import render
from stories.models import Story
from contact.models import Contact

# Create your views here.
def home_view(request):
    latest_stories = Story.objects.order_by('-created_at')[:3] 
    messages = Contact.objects.order_by('-created_at')
    return render(request, 'main/home.html', {
        'latest_stories': latest_stories,
        'messages': messages
    })

def about_view(request):
    return render(request, 'main/about.html')