from django.contrib import admin
from .models import UserProfile, CompanionProfile


admin.site.register(UserProfile)
admin.site.register(CompanionProfile)