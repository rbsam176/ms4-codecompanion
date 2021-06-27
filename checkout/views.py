from django.shortcuts import get_object_or_404, redirect, render, reverse, HttpResponse
from django.views.decorators.http import require_POST
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

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'email_address': request.POST['email_address'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            flat_bag = []
            for item in bag.items():
                try:
                    service = Service.objects.get(pk=item[0])
                    if len(item[1]) > 1:
                        for sub_item in item[1]:
                            companion = User.objects.filter(username=sub_item['companion_selected']).values('username')
                            sub_item['companion_selected'] = companion
                            flat_bag.append((service, sub_item))
                    else:
                        companion = User.objects.filter(username=item[1][0]['companion_selected']).values('username')
                        item[1][0]['companion_selected'] = companion
                        flat_bag.append((service, item[1][0]))

                except Service.DoesNotExist:
                    messages.error(request, (
                        "A service in your bag was not found in the database. "
                        "Please contact us via the email address at the bottom of this page for assistance.")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            
            print(flat_bag)

            for x in flat_bag:
                order_line_item = OrderLineItem(
                    service=x[0],
                    quantity=x[1]['quantity'],
                    companion_selected=x[1]['companion_selected'],
                    day_selected=x[1]['day_selected'],
                    order=order,
                )
                order_line_item.save()

            # request.session['save_info'] = 'save-info' in request.POST 
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

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

    messages.success(request, f'Order successfull! Your order number is {order_number}. \
        An email will be sent to {order.email_address} with confirmation')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
    }

    return render(request, template, context)