from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages

from .models import Service, PriceType
from .forms import ServiceForm

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


def add_service(request):
	""" Add a service to the store """
	if request.method == 'POST':
		form = ServiceForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully added service')
			return redirect(reverse('add_service'))
		else:
			messages.error(request, 'Failed to add service')
	else:
		form = ServiceForm()
		
	template = 'services/add_service.html'
	context = {
		'form': form,
	}

	return render(request, template, context)