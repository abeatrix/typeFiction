from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=25)
    image = models.CharField(max_length=250)
    following = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="follower")

    def __str__(self):
        return self.user.username

# Create Profile when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# Category
class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Story
class Story(models.Model):
    title = models.TextField(max_length=20)
    description = models.TextField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, symmetrical=False, default=0, related_name="likes")
    watchlist = models.ManyToManyField(User, symmetrical=False, default=0, related_name="watches")

    def __str__(self):
        return self.description

# Chapter
class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    chapter = models.CharField(max_length=250)
    content = models.TextField(max_length=9999)
    
    def __str__(self):
        return self.chapter