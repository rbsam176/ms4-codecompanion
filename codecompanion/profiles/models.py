from django.db import models
from django.contrib.auth.models import User

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
    account_type = models.ForeignKey('AccountType', null=True, blank=True, on_delete=models.SET_NULL)
    