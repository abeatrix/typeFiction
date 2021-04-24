from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Profile
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
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
