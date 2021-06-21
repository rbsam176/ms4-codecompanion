from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class AccountType(models.Model):
    type = models.CharField(max_length=254)
    friendly_type = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_type(self):
        return self.friendly_name


class UserProfile(models.Model):
    """ A user profile model for customer accounts """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    account_type = models.ForeignKey('AccountType', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update user profile """
    if created:
        UserProfile.objects.create(user=instance)
    # If already exists, just save
    instance.userprofile.save()