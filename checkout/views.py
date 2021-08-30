from django.shortcuts import get_object_or_404, redirect, render, reverse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .forms import OrderForm
from .models import Order, OrderLineItem
from services.models import Service
from bag.context_processors import bag_contents
from profiles.models import UserProfile, CompanionProfile

import stripe
import json
from datetime import datetime
import pytz


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
            'bag': json.dumps(request.session.get('bag', {})),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment is not able to be processed \
            at this time. Try again, or contact us using our email at the bottom \
                of the page.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'notes': request.POST['notes'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            # EXTRACT BAG CONTENTS INTO INDIVIDUAL ITEMS
            flattened = []
            for x in bag.keys():
                if len(bag[x]) > 1:
                    for y in bag[x]:

                        try:
                            y['companion_selected'] = User.objects.get(username=y['companion_selected'])
                        except User.DoesNotExist:
                            messages.error(request, (
                                "There was an issue with your account."
                                "Please contact us via the email address at the bottom of this page for assistance.")
                            )
                            order.delete()
                            return redirect(reverse('view_bag'))

                        try:
                            y['service'] = Service.objects.get(name=x)
                            flattened.append(y)
                        except Service.DoesNotExist: 
                            messages.error(request, (
                                "A service in your bag was not found in the database. "
                                "Please contact us via the email address at the bottom of this page for assistance.")
                            )
                            order.delete()
                            return redirect(reverse('view_bag'))
                else:
                    try:
                        bag[x][0]['companion_selected'] = User.objects.get(username=bag[x][0]['companion_selected'])
                    except User.DoesNotExist:
                        messages.error(request, (
                            "There was an issue with your account."
                            "Please contact us via the email address at the bottom of this page for assistance.")
                        )
                        order.delete()
                        return redirect(reverse('view_bag'))
                    try:
                        bag[x][0]['service'] = Service.objects.get(name=x)
                        flattened.append(bag[x][0])
                    except Service.DoesNotExist: 
                        messages.error(request, (
                            "A service in your bag was not found in the database. "
                            "Please contact us via the email address at the bottom of this page for assistance.")
                        )
                        order.delete()
                        return redirect(reverse('view_bag'))

            for x in flattened:
                # PARSE TIME STRING
                start_dt_naive = datetime.strptime(x['start_datetime'], '%Y-%m-%d %H:%M:%S')
                end_dt_naive = datetime.strptime(x['end_datetime'], '%Y-%m-%d %H:%M:%S')
                # SET IT TO UK
                timezone = pytz.timezone("Europe/London")
                start_dt_uk = timezone.localize(start_dt_naive, is_dst=None)
                end_dt_uk = timezone.localize(end_dt_naive, is_dst=None)
                # CONVERT TO UTC
                start_dt_aware = start_dt_uk.astimezone(pytz.utc)
                end_dt_aware = end_dt_uk.astimezone(pytz.utc)
                
                order_line_item = OrderLineItem(
                    service=x['service'],
                    companion_selected=x['companion_selected'],
                    start_datetime=start_dt_aware,
                    end_datetime=end_dt_aware,
                    order=order,
                    lineitem_total=x['service'].price,
                )
                order_line_item.save()
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, "There was an error in the form. Please verify all information is correct")
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There is nothing in your bag at this time")
            return redirect(reverse('services'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key missing.')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


@login_required
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

    messages.success(request, f'Order successfull! Your order number is {order_number}. \
        A confirmation email will be sent.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
    }

    return render(request, template, context)