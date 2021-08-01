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
		# date_selection = request.GET['date_selection']
		date_selection = datetime.datetime.strptime(request.GET['date_selection'], "%Y-%m-%d").date()
		weekday_selection = calendar.day_name[date_selection.weekday()].lower() + "_available"

		service_selection = request.GET['service_selection'].replace(" ", "_").lower() + "_offered"

		# SOURCE: https://stackoverflow.com/a/9122180
		# return list of companions working on selected day and offers selected service
		companion_match = CompanionProfile.objects.filter(**{weekday_selection:True}, **{service_selection:True}).values_list('user', flat=True)

		# UNPACK USERNAMES TO BE RETURNED TO VIEW
		# usernames = []
		# for list in companion_match:
		# 	for id in list:
		# 		usernames.append(str(User.objects.get(id=id)))



		# GETS ALL POSSIBLE TIME SLOTS -------
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

		# END ---------


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
							print('available')
						elif requested_end_time == existing_start_time and requested_start_time <= existing_start_time:
							if requested_end_time <= existing_start_time or requested_start_time >= existing_end_time:
								available_slots.append({
									'start_time': requested_start_time.strftime('%H:%M'),
									'end_time': requested_end_time.strftime('%H:%M'),
								})
								print('available')
							else:
								print('not available')
						elif requested_start_time == existing_end_time:
							if requested_start_time >= existing_end_time:
								available_slots.append({
									'start_time': requested_start_time.strftime('%H:%M'),
									'end_time': requested_end_time.strftime('%H:%M'),
								})
								print('available')
							else:
								print('not available')
						else:
							print('not available')

			return available_slots

		available_companions = []
		if len(companion_match) > 1:
			for id in companion_match:
				companion = User.objects.get(id=id)
				username = companion.username
				if len(check_availability(companion)) > 0:
					available_companions.append({str(username): check_availability(companion)})
		else:
			companion = User.objects.get(id=companion_match[0])
			username = companion.username
			if len(check_availability(companion)) > 0:
				available_companions.append({str(username): check_availability(companion)})

		print(available_companions)






		# got the orders with times from all available companions
		# wrap this up into an object that can be sent to the view
		# only send if that day has available slots
		# if view doesn't receive it doesn't display companion
		# if view does receive then it displays companions available time slots
		
		# for x in companion_orders:
		# 	print(x.start_datetime)

		









		data = {
			'available_companions': available_companions
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

	def get_day_initial(weekday):
		initials = {
			0: 'MON',
			1: 'TUE',
			2: 'WED',
			3: 'THU',
			4: 'FRI',
			5: 'SAT',
			6: 'SUN',
		}

		if initials[weekday]:
			return initials[weekday]
	
	def get_month_initial(month):
		initials = {
			1: 'JAN',
			2: 'FEB',
			3: 'MAR',
			4: 'APR',
			5: 'MAY',
			6: 'JUN',
			7: 'JUL',
			8: 'AUG',
			9: 'SEP',
			10: 'OCT',
			11: 'NOV',
			12: 'DEC',
		}

		if initials[month]:
			return initials[month]
	
	today = datetime.date.today()
	next_5_days = {}
	for date in range(7):
		if (today + datetime.timedelta(days=date)).weekday() != 5 and (today + datetime.timedelta(days=date)).weekday() != 6:
			if len(next_5_days) <= 5:
				date_adding = today + datetime.timedelta(days=date)
				next_5_days[date_adding] = {'day_index': date_adding.weekday(), 'day': get_day_initial(date_adding.weekday()), 'date': date_adding.day, 'month_index': date_adding.month, 'month': get_month_initial(date_adding.month)}
	
	service = get_object_or_404(Service, endpoint=endpoint)

	
	open_hour = datetime.datetime(1, 1, 1, 9,00,00)
	close_hour = datetime.datetime(1, 1, 1, 18,00,00)
	minutes_open = datetime.timedelta(minutes=int((close_hour - open_hour).total_seconds() / 60))

	num_sessions_per_day = int(minutes_open / (datetime.timedelta(minutes=30)))
	slots = []
	
	for x in range(num_sessions_per_day*2):
		if len(slots) > 0:
			last_index = len(slots)-1
			increment = slots[last_index]['start_time'] + datetime.timedelta(minutes=30)
			# 1 HOUR INCREMENTS: slots.append({'start_time': slots[last_index]['end_time'], 'end_time': slots[last_index]['end_time'] + datetime.timedelta(hours=float(service.duration))})
			if not increment + datetime.timedelta(hours=float(service.duration)) > close_hour:
				slots.append({'start_time': increment, 'end_time': increment + datetime.timedelta(hours=float(service.duration))})
		else:
			slots.append({'start_time': open_hour, 'end_time': open_hour + datetime.timedelta(hours=float(service.duration)),})

	time_slots = []
	for i in slots:
		time_slots.append({'start_time': i['start_time'].strftime('%H:%M'), 'end_time': i['end_time'].strftime('%H:%M')})

	context = {
		'service': service,
		'days_count': days_count,
		'next_5_days': next_5_days,
		'time_slots': time_slots,
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