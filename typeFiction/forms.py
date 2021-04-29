from django.forms import ModelForm, ModelChoiceField
from .models import Profile, Category, Story, Chapter
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

# For for creating Story
class Story_Form(ModelForm):
    title = forms.CharField(max_length= 50, required=True)

    class Meta:
        model = Story
        fields = ['title', 'description', 'category']

# For for creating Chapter in Story
class Chapter_Form(ModelForm):
    chapter = forms.CharField(max_length= 250, required=True)

    class Meta:
        model = Chapter
        fields = ['chapter', 'content']
