from django.contrib import admin
from .models import PriceType, Service

# Register your models here.
admin.site.register(PriceType)
admin.site.register(Service)