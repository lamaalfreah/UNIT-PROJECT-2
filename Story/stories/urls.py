from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('stories/all/', views.all_stories_view, name='all_stories'),
    path('stories/<int:story_id>/detail/', views.story_detail_view, name='story_detail'),
    path('stories/<int:story_id>/update/', views.update_story_view, name='update_story'),
    path('stories/<int:story_id>/delete/', views.delete_story_view, name='delete_story'),
    path('stories/new/', views.add_story_view, name='add_story'),
    path('stories/search/', views.search_stories_view, name='search_story'),
    path('<int:pk>/tts/', views.story_tts, name='story_tts'),
]