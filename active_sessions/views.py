from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from checkout.models import Order, OrderLineItem
import datetime
import pytz


def redirect_services(request):
	return redirect('/profile')


@login_required
def active_sessions(request, order_number):
    """ A view providing Jitsi integration for
    students to communicate with Companions """
    account = get_object_or_404(User, username=request.user)
    order = get_object_or_404(Order, order_number=order_number)

    # CHECK FOR ACTIVE SESSIONS
    lineitems = OrderLineItem.objects.filter(order=order)
    session = None

    current_ts = datetime.datetime.now(tz=pytz.timezone('UTC'))

    for item in lineitems:
        seconds_until = (item.start_datetime - current_ts).total_seconds()
        # IF WITHIN 5 MIN OF SESSION START TIME, OR CURRENT TIME IS START TIME,
        # OR CURRENT TIME IS BETWEEN START AND END TIME
        if (seconds_until < 300 or current_ts == item.start_datetime or
            current_ts > item.start_datetime and current_ts < item.end_datetime):
            session = item
    if session:
        context = {
            'account': account,
            'order': order,
            'session': session,
        }
        return render(request, 'active_sessions/active_sessions.html', context)
    else:
        return redirect('/profile')