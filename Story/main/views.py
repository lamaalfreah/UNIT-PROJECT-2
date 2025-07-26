from django.shortcuts import render
from stories.models import Story

# Create your views here.
def home_view(request):
    latest_stories = Story.objects.order_by('-created_at')[:3] 
    return render(request, 'main/home.html', {'latest_stories': latest_stories})

def about_view(request):
    return render(request, 'main/about.html')
