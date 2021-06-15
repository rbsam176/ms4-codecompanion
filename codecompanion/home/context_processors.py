from services.models import Service

def add_variable_to_context(request):

    services = Service.objects.all()
    return {
        'services': services,
    }