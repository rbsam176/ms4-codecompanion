from django.shortcuts import get_object_or_404, render, redirect
from .models import Service

def redirect_services(request):
	return redirect('/services/compare-services')


def compare_services(request):
	""" A view to return the Compare Services page """

	return render(request, 'services/compare_services.html')


def service_detail(request, endpoint):
	""" A view to return the view of each service """

	service = get_object_or_404(Service, endpoint=endpoint)

	context = {
		'service': service,
	}

	return render(request, 'services/service_detail.html', context)