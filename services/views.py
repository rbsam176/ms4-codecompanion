import datetime
import pytz
import math, calendar
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse


from profiles.models import UserProfile, CompanionProfile
from checkout.models import Order, OrderLineItem

from .models import Service, PriceType
from .forms import ServiceForm

def redirect_services(request):
	return redirect('/services/compare-services')


def compare_services(request):
	""" A view to return the Compare Services page """

	return render(request, 'services/compare_services.html')


def companion_availability_check(request):
	if request.method == 'GET':
		date_selection = datetime.datetime.strptime(request.GET['date_selection'], "%Y-%m-%d").date()
		weekday_selection = calendar.day_name[date_selection.weekday()].lower() + "_available"
		service_selection = request.GET['service_selection'].replace(" ", "_").lower() + "_offered"

		# SOURCE: https://stackoverflow.com/a/9122180
		# return list of companions working on selected day and offers selected service
		companion_match = CompanionProfile.objects.filter(**{weekday_selection:True}, **{service_selection:True}).values_list('user', flat=True)

		# GETS ALL POSSIBLE TIME SLOTS
		service = Service.objects.get(name=request.GET['service_selection'])
		open_hour = datetime.datetime.combine(date_selection, datetime.time(9, 00))
		close_hour = datetime.datetime.combine(date_selection, datetime.time(18, 00))
		hours_open = datetime.timedelta(minutes=int((close_hour - open_hour).total_seconds() / 60))
		num_sessions_per_day = int(hours_open / (datetime.timedelta(minutes=30)))
		slots = []
		for x in range(num_sessions_per_day*2):
			if len(slots) > 0:
				last_index = len(slots)-1
				increment = slots[last_index]['start_time'] + datetime.timedelta(minutes=30)
				if not increment + datetime.timedelta(hours=float(service.duration)) > close_hour:
					slots.append({'start_time': increment, 'end_time': increment + datetime.timedelta(hours=float(service.duration))})
			else:
				slots.append({'start_time': open_hour, 'end_time': open_hour + datetime.timedelta(hours=float(service.duration)),})


		def check_availability(companion):
			companion_orders = OrderLineItem.objects.filter(companion_selected=companion)
			available_slots = []
			for slot in slots:
				for order in companion_orders:
					existing_start_time = order.start_datetime
					existing_end_time = order.end_datetime
					requested_start_time_naive = slot['start_time']
					requested_end_time_naive = slot['end_time']
					timezone = pytz.timezone("UTC")
					requested_start_time = timezone.localize(requested_start_time_naive)
					requested_end_time = timezone.localize(requested_end_time_naive)
					if existing_start_time is not None and existing_end_time is not None:
						if requested_start_time > existing_end_time or requested_end_time < existing_start_time:
							available_slots.append({
								'start_time': requested_start_time.strftime('%H:%M'),
								'end_time': requested_end_time.strftime('%H:%M'),
							})
						elif requested_end_time == existing_start_time and requested_start_time <= existing_start_time:
							if requested_end_time <= existing_start_time or requested_start_time >= existing_end_time:
								available_slots.append({
									'start_time': requested_start_time.strftime('%H:%M'),
									'end_time': requested_end_time.strftime('%H:%M'),
								})
						elif requested_start_time == existing_end_time:
							if requested_start_time >= existing_end_time:
								available_slots.append({
									'start_time': requested_start_time.strftime('%H:%M'),
									'end_time': requested_end_time.strftime('%H:%M'),
								})
			return available_slots

		available_companions = []
		if len(companion_match) > 1:
			for id in companion_match:
				companion = User.objects.get(id=id)
				username = companion.username
				if len(check_availability(companion)) > 0:
					available_companions.append({str(username): check_availability(companion)})
		elif len(companion_match) == 1:
			companion = User.objects.get(id=companion_match[0])
			username = companion.username
			if len(check_availability(companion)) > 0:
				available_companions.append({str(username): check_availability(companion)})

		data = {
			'available_companions': available_companions
		}
		return JsonResponse(data, safe=False)


def service_detail(request, endpoint):
	""" A view to return the view of each service and bookable dates """
	service = get_object_or_404(Service, endpoint=endpoint)
	today = datetime.date.today()
	next_5_days = {}
	for date in range(7):
		if (today + datetime.timedelta(days=date)).weekday() != 5 and (today + datetime.timedelta(days=date)).weekday() != 6:
			if len(next_5_days) <= 5:
				date_adding = today + datetime.timedelta(days=date)
				next_5_days[date_adding] = {'day_index': date_adding.weekday(), 'day': date_adding.strftime("%a").upper(), 'date': date_adding.day, 'month_index': date_adding.month, 'month': date_adding.strftime('%b').upper()}
	
	service_offered = str(service).replace(" ", "_").lower() + "_offered"

	for key, value in next_5_days.items():
		day = key.strftime("%A").lower() + "_available"
		companion_match = CompanionProfile.objects.filter(**{str(day):True}, **{service_offered:True}).values_list('user', flat=True)
		for x in companion_match:
			if key in next_5_days:
				next_5_days[key]['companions_available'] = True


	context = {
		'service': service,
		'next_5_days': next_5_days,
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