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


def edit_service(request, endpoint):
	""" Edit a service in the store """
	service = get_object_or_404(Service, endpoint=endpoint)
	if request.method == 'POST':
		form = ServiceForm(request.POST, instance=service)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated service')
			return redirect(reverse('service_detail', args=[endpoint]))
		else:
			messages.error(request, 'Failed to update service')
	else:
		form = ServiceForm(instance=service)
		messages.info(request, f'You are editing {service.name}')

	template = 'services/edit_service.html'
	context = {
		'form': form,
		'service': service,
	}

	return render(request, template, context)