from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm, CompanionCheck
from .models import UserProfile

from checkout.models import Order

@login_required
def profile(request):
	""" Display user profile """

	# user accounts
	account = get_object_or_404(User, username=request.user)
	profile = get_object_or_404(UserProfile, user=request.user)
	
	# forms
	user_form = UserForm(request.POST or None, instance=account)
	companion_availability = UserProfileForm(request.POST or None, instance=profile)
	companion_check = CompanionCheck(request.POST or None, instance=profile)

	# post logic
	if request.method == 'POST':

		if user_form.is_valid():
			print('user form valid')
			user_form.save()
		
		if companion_availability.is_valid():
			print('companion form valid')
			# if not companion, clear availability
			if not request.POST.get('is_companion'):
				profile.monday_available = False
				profile.tuesday_available = False
				profile.wednesday_available = False
				profile.thursday_available = False
				profile.friday_available = False
			companion_availability.save()
		
		messages.success(request, 'Profile updated successfully')


	if profile.is_companion:
		companion_form = companion_availability
	else:
		companion_form = companion_check

	orders = profile.orders.all()

	template = 'profiles/profile.html'
	context = {
		'account': account,
		'user_form': user_form,
		'companion_form': companion_form,
		'orders': orders,
	}

	return render(request, template, context)


def order_history(request, order_number):
	order = get_object_or_404(Order, order_number=order_number)

	messages.info(request, (
		f'This is a past order confirmation for order number {order_number}. \
			A confirmaiton email should have been sent on the order date'
	))

	template = 'checkout/checkout_success.html'
	context = {
		'order': order,
	}

	return render(request, template, context)