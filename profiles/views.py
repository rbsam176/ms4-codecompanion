from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm, CompanionCheck
from .models import UserProfile, CompanionProfile

from checkout.models import Order

@login_required
def profile(request):
	""" Display user profile """

	# user accounts
	account = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(UserProfile, user=request.user)
	
	# forms
	user_form = UserForm(request.POST or None, instance=account) # allauth standard
	companion_check = CompanionCheck(request.POST or None, instance=profile) # custom user with companion boolean

	# post logic
	if request.method == 'POST':
		if user_form.is_valid() and companion_check.is_valid():
			user_form.save()
			companion_check.save()

			if request.POST.get('is_companion'):
				print('is companion enabled')
				try:
					companion_profile = get_object_or_404(CompanionProfile, user=request.user)
					companion_availability = UserProfileForm(request.POST or None, instance=companion_profile)
					if companion_availability.is_valid():
						companion_availability.save()
						messages.success(request, 'Availability updated successfully')
					pass
				except:
					# convert user to companion
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
		}
	else:
		context = {
			'account': account,
			'user_form': user_form,
			'companion_check': companion_check,
			'orders': orders,
		}

	return render(request, template, context)


def order_history(request, order_number):
	order = get_object_or_404(Order, order_number=order_number)
	account = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(UserProfile, user=request.user)

	# template = 'checkout/checkout_success.html'
	template = 'profiles/view_order.html'
	context = {
		'order': order,
		'account': account,
	}

	return render(request, template, context)