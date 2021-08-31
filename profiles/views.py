from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User

from .forms import UserProfileForm, UserForm, CompanionCheck
from .models import UserProfile, CompanionProfile

from django.template.loader import render_to_string

from checkout.models import Order, OrderLineItem
from services.models import Service

import datetime
import pytz


def ajax_pagination(request):
	profile = get_object_or_404(UserProfile, user=request.user)
	orders = profile.orders.all().order_by('-date')
	p = Paginator(orders, 3)

	if request.method == 'GET':
		if p.page(int(request.GET['page_num'])).has_next():
			page_num = int(request.GET['page_num']) + 1
			has_next = p.page(page_num).has_next()
			desktop = render_to_string(
				"profiles/orders_desktop.html", {"desktop": p.page(page_num).object_list}
			)
			mobile = render_to_string(
				"profiles/orders_mobile.html", {"mobile": p.page(page_num).object_list}
			)
			data = {
				'desktop': desktop,
				'mobile': mobile,
				'page_num': page_num,
				'has_next': has_next,
			}
		else:
			page_num = None
			data = {
				'page_num': page_num,
			}

		return JsonResponse(data, safe=False)


@login_required
def profile(request):
	""" Display user profile """
	account = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(UserProfile, user=request.user)

	user_form = UserForm(request.POST or None, instance=account)
	companion_check = CompanionCheck(request.POST or None, instance=profile)

	companion_services = []
	if profile.is_companion:
		companion_profile = get_object_or_404(CompanionProfile, user=request.user)
		for service in Service.objects.filter(companion=companion_profile):
			companion_services.append(service)

	if request.method == 'POST':
		if user_form.is_valid() and companion_check.is_valid():
			user_form.save()
			companion_check.save()
			if request.POST.get('is_companion'):
				try:
					companion_profile = get_object_or_404(CompanionProfile, user=request.user)

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
							pre_existing = (
								OrderLineItem.objects.filter(companion_selected=companion_profile)
								.filter(start_datetime__gte=now)
								.filter(service=service)
							)
							# IF THEY DO, DEFINE WARNING MESSAGE
							if len(pre_existing) > 0:
								plural = 's' if len(pre_existing) > 1 else ''
								pre_existing_message = f"You had {len(pre_existing)} {service} \
									session{plural} coming up that have been cancelled."

					companion_availability = UserProfileForm(
						request.POST or None, instance=companion_profile
					)
					if companion_availability.is_valid():
						companion_availability.save()
						messages.success(request, 'Account updated successfully')
						# IF COMPANION IS UNCHECKING SERVICE AND HAS UPCOMING SESSIONS
						if pre_existing_message and len(pre_existing) > 0:
							messages.warning(request, pre_existing_message)
							pre_existing.delete()
				except:
					# CONVERT USER TO COMPANION
					new_companion = CompanionProfile(user=account)
					new_companion.save()
					messages.success(request, 'Converted profile to be companion')
			else:
				try:
					companion_profile = get_object_or_404(
						CompanionProfile, user=request.user
					)

					# CHECK IF COMPANION HAS UPCOMING SESSIONS BOOKED FOR THIS SERVICE
					now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
					existing_sessions = OrderLineItem.objects.filter(
						companion_selected=companion_profile
					).filter(start_datetime__gte=now)
					if len(existing_sessions) > 0:
						existing_sessions.delete()

					# IF USER IS COMPANION, DELETE
					companion_profile.delete()
					messages.warning(
						request,
						"You are no longer a companion, any existing upcoming sessions \
							have been cancelled.",
					)
				except:
					# IF USER IS NOT COMPANION, DO NOTHING
					messages.success(request, 'Updated profile successfully')
					pass

	# GET UPCOMING SESSIONS
	orders = profile.orders.all().order_by('-date')
	sessions = []
	for order in orders:
		for session in OrderLineItem.objects.filter(order=order):
			current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))
			# SECONDS BETWEEN CURRENT TIME AND START TIME
			seconds_until = (session.start_datetime - current_ts).total_seconds()
			if current_ts < session.start_datetime and seconds_until > 300:
				status = 'upcoming'
				sessions.append({
				'session': session,
				'status': status
				})
			if (current_ts == session.start_datetime or seconds_until < 300 and
				seconds_until > 0 or current_ts > session.start_datetime and
					current_ts < session.end_datetime):
				status = 'active'
				sessions.append({
				'session': session,
				'status': status
				})

	sessions = sorted(sessions, key=lambda k: k['session'].start_datetime)
	
	template = 'profiles/profile.html'

	p = Paginator(orders, 3)
	page1 = p.page(1)

	if profile.is_companion:
		companion_profile = get_object_or_404(CompanionProfile, user=request.user)
		companion_availability = UserProfileForm(
			request.POST or None, instance=companion_profile
		)

		# GET COMPANION UPCOMING SESSIONS
		now = datetime.datetime.now(tz=pytz.timezone('UTC'))
		companion_sessions = (
			OrderLineItem.objects.filter(companion_selected=companion_profile)
			.filter(start_datetime__gte=now)
			.order_by("start_datetime")
		)
		companion_sessions_formatted = []
		for session in companion_sessions:
			# SECONDS BETWEEN CURRENT TIME AND START TIME
			seconds_until = (session.start_datetime - now).total_seconds()

			if now < session.start_datetime and seconds_until > 300:
				status = 'upcoming'
				companion_sessions_formatted.append({
				'session': session,
				'status': status
				})

			if (now == session.start_datetime or seconds_until < 300 and
				seconds_until > 0 or now > session.start_datetime and
					now < session.end_datetime):
				status = 'active'
				companion_sessions_formatted.append({
				'session': session,
				'status': status
				})
		
		context = {
			'account': account,
			'profile': profile,
			'user_form': user_form,
			'companion_availability': companion_availability,
			'companion_check': companion_check,
			'orders': page1,
			'orders_length': p.count,
			'sessions': sessions,
			'companion_services': companion_services,
			'companion_sessions': companion_sessions_formatted,
		}
	else:
		context = {
			'account': account,
			'profile': profile,
			'user_form': user_form,
			'companion_check': companion_check,
			'orders': page1,
			'orders_length': p.count,
			'sessions': sessions,
			'companion_services': companion_services,
		}

	return render(request, template, context)


@login_required
def order_history(request, order_number):
	""" Display specific order info """
	order = get_object_or_404(Order, order_number=order_number)
	account = get_object_or_404(User, username=request.user)

	lineitems = OrderLineItem.objects.filter(order=order)

	current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))

	sessions = []

	current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))

	print(lineitems)

	for item in lineitems:
		# SECONDS BETWEEN CURRENT TIME AND START TIME
		seconds_until = (item.start_datetime - current_ts).total_seconds()

		if current_ts < item.start_datetime and seconds_until > 300:
			status = 'upcoming'
		elif (current_ts == item.start_datetime or seconds_until < 300 and
			   seconds_until > 0 or current_ts > item.start_datetime and
			   	current_ts < item.end_datetime):
			status = 'active'
		else:
			status = 'expired'

		sessions.append({
			'lineitem': item,
			'status': status
			})
	
	print(sessions)

	template = 'profiles/view_order.html'
	context = {
		'order': order,
		'account': account,
		'lineitems': sessions,
	}

	return render(request, template, context)