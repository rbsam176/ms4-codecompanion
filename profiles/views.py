from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm
from .models import UserProfile

from checkout.models import Order

@login_required
def profile(request):
	""" Display user profile """
	profile = get_object_or_404(UserProfile, user=request.user)

	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=profile)
		if form.is_valid():
			if request.POST.get('is_companion'):
				request.user.is_staff=True
				request.user.save()
			form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Update failed')
	else:
		form = UserProfileForm(instance=profile)
		
	orders = profile.orders.all()

	template = 'profiles/profile.html'
	context = {
		'profile': profile,
		'form': form,
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