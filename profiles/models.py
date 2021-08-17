from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CompanionProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    peer_programming_offered = models.BooleanField(default=False)
    code_review_offered = models.BooleanField(default=False)
    troubleshooting_offered = models.BooleanField(default=False)
    whiteboarding_session_offered = models.BooleanField(default=False)
    interview_prep_offered = models.BooleanField(default=False)
    deployment_assist_offered = models.BooleanField(default=False)
    monday_available = models.BooleanField(default=False)
    tuesday_available = models.BooleanField(default=False)
    wednesday_available = models.BooleanField(default=False)
    thursday_available = models.BooleanField(default=False)
    friday_available = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    
    def full_name(self):
        full_name = self.user.first_name + " " + self.user.last_name
        return full_name


class UserProfile(models.Model):
    """ A user profile model for customer accounts """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_companion = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update user profile """
    if created:
        UserProfile.objects.create(user=instance)
    # If already exists, just save
    instance.userprofile.save()