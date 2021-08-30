from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta

from services.models import Service


@login_required
def view_bag(request):
	""" A view to return the shopping bag """
	return render(request, 'bag/bag.html')


@login_required
def add_to_bag(request, service_name):
    """ Add the clicked service to the shopping bag """
    service = Service.objects.get(pk=service_name)
    redirect_url = request.POST.get('redirect_url')
    companion_selected = request.POST.get('companionSelection')

    if request.POST.get('date-selection') and request.POST.get('time-selection'):
        date = request.POST.get('date-selection')
        start_time = request.POST.get('time-selection')
        datetime_combined = f'{date} {start_time}:00.000000'
        start_datetime = datetime.strptime(datetime_combined, '%Y-%m-%d %H:%M:%S.%f')
        end_datetime = start_datetime + timedelta(hours=float(service.duration))
    else:
        messages.error(request, "You haven't completed your selection")
        return redirect(redirect_url)

    bag = request.session.get('bag', {})

    # PREVENTS USER BOOKING SESSION WITH THEMSELF
    if str(companion_selected) == str(request.user):
        messages.error(request, 'You are not able to book a session with yourself')
        return redirect(redirect_url)

    order = {
        'start_datetime': str(start_datetime),
        'end_datetime': str(end_datetime),
        'companion_selected': companion_selected,
    }

    # IF BAG HAS SERVICE IN IT ALREADY
    if service_name in list(bag.keys()):
        # LOOP THROUGH ALL ORDERS WITH THE SAME SERVICE NAME
        for x in bag[service_name]:
            # IF THE ORDER HAS THE SAME COMPANION AND DATETIME, FAIL
            if (x['start_datetime'] == str(start_datetime) and
                x['companion_selected'] == companion_selected):
                messages.error(request, f'Already added "{service.name}" at\
                    the selected time to your bag')
                return redirect(redirect_url)
            # ELSE ADD TO EXISTING ORDERS LIST
            else:
                bag[service_name].append(order)
                messages.success(request, f'Added "{service.name}" to your bag')
                request.session['bag'] = bag
                return redirect(redirect_url)
    # IF BAG DOES NOT HAVE SERVICE IN IT ALREADY
    else:
        bag[service_name] = [order]
        messages.success(request, f'Added "{service.name}" to your bag')
        request.session['bag'] = bag
        return redirect(redirect_url)
    
    return redirect(redirect_url)


@login_required
def remove_from_bag(request, service_name):
    """ Remove item from the shopping bag """
    name = service_name.split("_")[0]
    start_datetime = service_name.split("_")[1]
    companion = service_name.split("_")[2]
    try:
        bag = request.session.get('bag', {})
        for item in bag[name]:
            if (item['start_datetime'] == start_datetime and
                item['companion_selected'] == companion):
                if len(bag[name]) == 1:
                    del bag[name]
                elif len(bag[name]) > 1:
                    deletion_index = bag[name].index(item)
                    del bag[name][deletion_index]
        request.session['bag'] = bag
        messages.warning(request, f'Removed "{name}" from your bag')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'An error occured when attempting to remove\
            "{service_name}" from your bag. Error code {e}')
        return HttpResponse(status=500)