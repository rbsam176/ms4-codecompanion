from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm, CompanionCheck
from .models import UserProfile, CompanionProfile

from checkout.models import Order, OrderLineItem
from services.models import Service

import datetime
import pytz


@login_required
def profile(request):
	""" Display user profile """

	# user accounts
	account = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(UserProfile, user=request.user)
	companion_profile = get_object_or_404(CompanionProfile, user=request.user)
	
	# forms
	user_form = UserForm(request.POST or None, instance=account) # allauth standard
	companion_check = CompanionCheck(request.POST or None, instance=profile) # custom user with companion boolean

	companion_services = []
	for service in Service.objects.filter(companion=companion_profile):
		companion_services.append(service)

	# post logic
	if request.method == 'POST':
		if user_form.is_valid() and companion_check.is_valid():
			user_form.save()
			companion_check.save()

			if request.POST.get('is_companion'):
				print('is companion enabled')
				try:
					# companion_profile = get_object_or_404(CompanionProfile, user=request.user)

					# LIST OF ALL SERVICES
					all_services = Service.objects.all()
					# LIST OF ALL SERVICES CHECKED ON FORM SUBMISSION
					services_checked = []
					for service in request.POST.getlist('service_offered'):
						services_checked.append(get_object_or_404(Service, name=service))

					# DEFINE EMPTY MESSAGE
					pre_existing_message = None

					# ADD/REMOVE COMPANION FROM SERVICE OBJECT
					for service in all_services:
						# ADD
						if service in services_checked and service not in companion_services:
							service_obj = get_object_or_404(Service, name=service)
							service_obj.companion.add(companion_profile)
							companion_services.append(service_obj)
						# REMOVE
						if service in companion_services and service not in services_checked:
							service.companion.remove(companion_profile)
							companion_services.remove(service)
							# CHECK IF COMPANION HAS UPCOMING SESSIONS BOOKED FOR THIS SERVICE
							now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
							pre_existing = len(OrderLineItem.objects.filter(companion_selected=companion_profile).filter(start_datetime__gte=now).filter(service=service))
							# IF THEY DO, DEFINE WARNING MESSAGE
							if pre_existing > 0:
								plural = 's' if pre_existing > 1 else ''
								pre_existing_message = f'You have {pre_existing} {service} session{plural} coming up that you will still be liable for. Please contact us to discuss cancelling these sessions.'

					companion_availability = UserProfileForm(request.POST or None, instance=companion_profile)
					if companion_availability.is_valid():
						companion_availability.save()
						messages.success(request, 'Account updated successfully')
						# IF COMPANION IS UNCHECKING SERVICE AND HAS UPCOMING SESSIONS
						if pre_existing_message:
							messages.warning(request, pre_existing_message)
				except:
					# CONVERT USER TO COMPANION
					new_companion = CompanionProfile(user=account)
					new_companion.save()
					messages.success(request, 'Converted profile to be companion')
			else:
				print('is companion NOT enabled')
				# if companion checkbox unchecked
				try:
					companion_profile = get_object_or_404(CompanionProfile, user=request.user)
					# if user is companion, delete
					companion_profile.delete()
					messages.warning(request, 'You are no longer a companion')
				except:
					# if user is not companion, do nothing
					messages.success(request, 'Updated profile successfully')
					pass

	orders = profile.orders.all().order_by('-date')

	sessions = []

	for order in orders:
		for session in OrderLineItem.objects.filter(order=order):
			current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))
			# SECONDS BETWEEN CURRENT TIME AND START TIME
			seconds_until = (session.start_datetime - current_ts).total_seconds()

			if current_ts < session.start_datetime:
				status = 'upcoming'
				sessions.append({
				'session': session,
				'status': status
				})
			if current_ts == session.start_datetime or seconds_until < 300 or current_ts > session.start_datetime and current_ts < session.end_datetime:
				status = 'active'
				sessions.append({
				'session': session,
				'status': status
				})


	template = 'profiles/profile.html'

	if profile.is_companion:
		companion_profile = get_object_or_404(CompanionProfile, user=request.user)
		companion_availability = UserProfileForm(request.POST or None, instance=companion_profile)
		context = {
			'account': account,
			'user_form': user_form,
			'companion_availability': companion_availability,
			'companion_check': companion_check,
			'orders': orders,
			'sessions': sessions,
			'companion_services': companion_services,
		}
	else:
		context = {
			'account': account,
			'user_form': user_form,
			'companion_check': companion_check,
			'orders': orders,
			'sessions': sessions,
			'companion_services': companion_services,
		}

	return render(request, template, context)


def order_history(request, order_number):
	order = get_object_or_404(Order, order_number=order_number)
	account = get_object_or_404(User, username=request.user)

	lineitems = OrderLineItem.objects.filter(order=order)

	current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))

	sessions = []

	# current_ts = datetime.datetime.now(tz=pytz.timezone('Europe/London'))
	current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))

	for item in lineitems:
		# SECONDS BETWEEN CURRENT TIME AND START TIME
		seconds_until = (item.start_datetime - current_ts).total_seconds()

		print(seconds_until)

		
		if current_ts < item.start_datetime:
			status = 'upcoming'
		elif current_ts == item.start_datetime or seconds_until < 300 or current_ts > item.start_datetime and current_ts < item.end_datetime:
			status = 'active'
		else:
			status = 'expired'

		print(status)
		sessions.append({
			'lineitem': item,
			'status': status
			})

	template = 'profiles/view_order.html'
	context = {
		'order': order,
		'account': account,
		'lineitems': sessions,
	}

	return render(request, template, context)