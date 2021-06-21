from django.contrib import admin
from .models import AccountType, UserProfile


admin.site.register(AccountType)
admin.site.register(UserProfile)