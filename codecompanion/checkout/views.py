from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag at this time")
        return redirect(reverse('services'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': "pk_test_51J3lGyJNKRSX8nglocosYsPhCS7URkjyaTdlbIDI4E4XHXuhpUDWE6dDB5Yjdw9NhWpAM2ScQ7MFk5o5f0wYXyf700wZee66K7",
        'client_secret': "test client secret",
    }

    return render(request, template, context)
