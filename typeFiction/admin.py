from django.contrib import admin

# Register your models here.
from .models import User, Story, Profile, Category, Chapter, Comment

admin.site.register(Profile)
admin.site.register(Story)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(Comment)