from services.models import Service
from django.utils.timezone import template_localtime

def add_variable_to_context(request):

    services = Service.objects.all()
    return {
        'services': services,
    }