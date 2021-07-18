from django.contrib import admin
from .models import FaqCategory, FaqEntry, FaqQuestion

# Register your models here.
admin.site.register(FaqCategory)
admin.site.register(FaqEntry)
admin.site.register(FaqQuestion)