from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse


from profiles.models import UserProfile, CompanionProfile

from .models import Service, PriceType
from .forms import ServiceForm

def redirect_services(request):
	return redirect('/services/compare-services')


def compare_services(request):
	""" A view to return the Compare Services page """

	return render(request, 'services/compare_services.html')


def companion_availability_check(request):
	if request.method == 'GET':
			day_selection = request.GET['day_selection']
			service_selection = request.GET['service_selection']
			service_match_formatted = service_selection.replace(" ", "_").lower() + "_offered"

			# SOURCE: https://stackoverflow.com/a/9122180

			# return list of companions available on selected day and offers selected service
			companion_match = CompanionProfile.objects.filter(**{day_selection:True}, **{service_match_formatted:True}).values_list('user')

			# unpack usernames to be returned to view
			usernames = []
			for list in companion_match:
				for id in list:
					usernames.append(str(User.objects.get(id=id)))

			data = {
				'available_companions': usernames
			}
			return JsonResponse(data, safe=False)


def service_detail(request, endpoint):
	""" A view to return the view of each service """

	service_match_formatted = endpoint.replace("-", "_").lower() + "_offered"
	days = [
		'monday_available',
		'tuesday_available',
		'wednesday_available',
		'thursday_available',
		'friday_available',
	]
	days_count = {}
	for day in days:
		days_count[day] = CompanionProfile.objects.filter(**{service_match_formatted:True}, **{day:True}).count()

	
	service = get_object_or_404(Service, endpoint=endpoint)

	context = {
		'service': service,
		'days_count': days_count,
	}

	return render(request, 'services/service_detail.html', context)


@login_required
def add_service(request):
	""" Add a service to the store """
	if not request.user.is_superuser:
		messages.error(request, 'Sorry, only store owners can do that')
		return redirect(reverse('home'))

	if request.method == 'POST':
		form = ServiceForm(request.POST)
		if form.is_valid():
			service = form.save()
			messages.success(request, 'Successfully added service')
			return redirect(reverse('service_detail', args=[service.endpoint]))
		else:
			messages.error(request, 'Failed to add service')
	else:
		form = ServiceForm()
		
	template = 'services/add_service.html'
	context = {
		'form': form,
	}

	return render(request, template, context)


@login_required
def edit_service(request, endpoint):
	""" Edit a service in the store """
	if not request.user.is_superuser:
		messages.error(request, 'Sorry, only store owners can do that')
		return redirect(reverse('home'))

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


@login_required
def delete_service(request, endpoint):
	""" Delete a service in the store """
	if not request.user.is_superuser:
		messages.error(request, 'Sorry, only store owners can do that')
		return redirect(reverse('home'))
		
	service = get_object_or_404(Service, endpoint=endpoint)
	service.delete()
	messages.success(request, 'Service deleted')
	return redirect(reverse('compare_services'))