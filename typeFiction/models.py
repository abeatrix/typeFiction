from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=30)
    image = models.URLField()
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
    name = models.CharField(max_length=100, default=None)
    def __str__(self):
        return self.name

# Chapter
class Chapter(models.Model):
    chapter = models.CharField(max_length=100, default=None)
    content = models.TextField(max_length=9999, default=None)
    
    def __str__(self):
        return self.chapter
        
# Story
class Story(models.Model):
    title = models.TextField(max_length=50, default=None)
    description = models.TextField(max_length=250, default=None)
    cover = models.URLField()
    completed = models.BooleanField(default=False)
    chapters = models.ManyToManyField(Chapter)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category', default=None)
    post_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, symmetrical=False, default=0, related_name="likes")
    watchlist = models.ManyToManyField(User, symmetrical=False, default=0, related_name="watches")

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-post_date']

# COMMENTS
class Comment(models.Model):
    comment = models.TextField(max_length=500, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='replies', blank=True)

    def __str__(self):
        return f"{self.comment} posted {self.comment_date}"

    class Meta:
        ordering = ['-comment_date']