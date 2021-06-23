from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """ A user profile model for customer accounts """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_companion = models.BooleanField(default=False)
    monday_available = models.BooleanField(default=False)
    tuesday_available = models.BooleanField(default=False)
    wednesday_available = models.BooleanField(default=False)
    thursday_available = models.BooleanField(default=False)
    friday_available = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update user profile """
    if created:
        UserProfile.objects.create(user=instance)
    # If already exists, just save
    instance.userprofile.save()