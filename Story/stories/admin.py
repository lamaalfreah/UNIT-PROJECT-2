from django.contrib import admin

# Register your models here.
from .models import Story, Comment

admin.site.register(Story)
admin.site.register(Comment)