from django.contrib import admin
from .models import FaqCategory, FaqEntry

# Register your models here.
admin.site.register(FaqCategory)
admin.site.register(FaqEntry)