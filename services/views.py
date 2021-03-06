import datetime
import pytz
import calendar
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from profiles.models import CompanionProfile
from checkout.models import OrderLineItem
from .models import Service
from .forms import ServiceForm

def redirect_services(request):
	return redirect('/services/compare-services')


def compare_services(request):
	""" A view to return the Compare Services page """
	
	# CREATE DICT WITH SERVICE AND COUNT
	services_count = []
	for x in Service.objects.all():
		services_count.append(
			{'service': x, 'count': OrderLineItem.objects.filter(service=x).count()}
		)
	
	# SORT BY COUNT
	services_sorted = sorted(services_count, key=lambda k: k['count'], reverse=True) 

	# ONLY CONTAINS SERVICE OBJECTS
	services_ordered = []
	for y in services_sorted:
		services_ordered.append(Service.objects.get(name=y['service']))

	# SET DEFAULT VIEW AS MOST POPULAR
	all_services = services_ordered

	if request.GET:
		if 'sort' in request.GET:
			if request.GET['sort'] == 'ASC':
				all_services = Service.objects.all().order_by('price')
			elif request.GET['sort'] == 'DESC':
				all_services = Service.objects.all().order_by('-price')
			elif request.GET['sort'] == 'popular':
				all_services = 	services_ordered
			else:
				all_services = services_ordered

	return render(request, 'services/compare_services.html', {'all_services':all_services})


def generateTimeSlots(service, date=datetime.date.today()):
	# GETS ALL POSSIBLE TIME SLOTS
	timezone = pytz.timezone("UTC")

	open_hour = datetime.datetime.combine(date, datetime.time(8, 00))
	close_hour = datetime.datetime.combine(date, datetime.time(17, 00))

	hours_open = datetime.timedelta(minutes=int((close_hour - open_hour).total_seconds() / 60))
	num_sessions_per_day = int(hours_open / (datetime.timedelta(minutes=30)))
	slots = []
	for x in range(num_sessions_per_day*2):
		if len(slots) > 0:
			last_index = len(slots)-1
			increment = slots[last_index]['start_time'] + datetime.timedelta(minutes=30)
			if not increment + datetime.timedelta(hours=float(service.duration)) > timezone.localize(close_hour):
				slots.append(
					{'start_time': increment,
					'end_time': increment + datetime.timedelta(hours=float(service.duration))}
				)
		else:
			slots.append(
				{'start_time': timezone.localize(open_hour),
				'end_time': timezone.localize(open_hour) + datetime.timedelta(hours=float(service.duration))}
			)
	
	return slots


def companion_availability_check(request):
	if request.method == 'GET':
		timezone = pytz.timezone("UTC")
		date_selection = datetime.datetime.strptime(request.GET['date_selection'], "%Y-%m-%d").date()
		weekday_selection = calendar.day_name[date_selection.weekday()].lower() + "_available"

		# RETURNS LIST OF COMPANIONS WORKING ON SELECTED DAY AND OFFERS SELECTED SERVICE
		companion_match = (
			Service.objects.filter(name=request.GET["service_selection"])
			.filter(**{f"companion__{weekday_selection}": True})
			.values_list("companion", flat=True)
		)

		# GETS ALL POSSIBLE TIME SLOTS
		service = Service.objects.get(name=request.GET['service_selection'])


		def check_availability(companion, date):
			companion_orders = OrderLineItem.objects.filter(companion_selected=companion).filter(
				start_datetime__gte=date
			)
			available_slots = generateTimeSlots(service, date)

			for slot in available_slots:
				if len(companion_orders) > 0:
					for order in companion_orders:
						existing_start_time = order.start_datetime
						existing_end_time = order.end_datetime

						if existing_start_time is not None and existing_end_time is not None:
							if slot['start_time'] > existing_end_time or slot['end_time'] < existing_start_time:
								# NO CLASH
								pass
							elif slot['end_time'] == existing_start_time  and slot['start_time'] <= existing_start_time:
								if slot['end_time'] <= existing_start_time or slot['start_time'] >= existing_end_time:
									# NO CLASH
									pass
								else:
									slot['status'] = 'clash'
							elif slot['start_time'] == existing_end_time:
								if slot['start_time'] >= existing_end_time:
									# NO CLASH
									pass
								else:
									slot['status'] = 'clash'
							else:
								slot['status'] = 'clash'

				# DISABLE START TIMES EARLIER THAN CURRENT UTC TIME
				if slot['start_time'] <= datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
					if "status" in slot:
						if slot['status'] != 'expired':
							slot['status'] = 'expired'
					else:
						slot['status'] = 'expired'
			return available_slots

		dt = timezone.localize(datetime.datetime.combine(date_selection, datetime.time(0, 00)))

		available_companions = []
		if len(companion_match) > 1:
			for id in companion_match:
				companion = CompanionProfile.objects.get(id=id)
				username = companion.user.username
				if len(check_availability(companion, dt)) > 0:
					available_companions.append({str(username): check_availability(companion, dt)})
		if len(companion_match) == 1:
			companion = CompanionProfile.objects.get(id=companion_match[0])
			username = companion.user.username
			if len(check_availability(companion, dt)) > 0:
				available_companions.append({str(username): check_availability(companion, dt)})
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

	for key, value in next_5_days.items():
		day = key.strftime("%A").lower() + "_available"
		companion_match = (
			Service.objects.filter(name=service)
			.filter(**{f"companion__{day}": True})
			.values_list("companion", flat=True)
		)

		for x in companion_match:
			if key in next_5_days:
				next_5_days[key]['companions_available'] = True

	context = {
		'service': service,
		'next_5_days': next_5_days,
		'slots': generateTimeSlots(service),
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