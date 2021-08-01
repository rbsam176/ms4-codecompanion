from django.shortcuts import get_object_or_404, render, redirect, reverse, HttpResponse
from django.contrib import messages
from datetime import date, datetime, timedelta

from services.models import Service

# Create your views here.
def view_bag(request):
	""" A view to return the shopping bag """

	return render(request, 'bag/bag.html')

def add_to_bag(request, service_name):
    """ Add a quantity of the clicked service to the shopping bag """
    service = Service.objects.get(pk=service_name)

    companion_selected = request.POST.get('companionSelection')
    date = request.POST.get('date-selection')
    start_time = request.POST.get('time-selection')
    datetime_combined = f'{date} {start_time}:00.000000'
    start_datetime = datetime.strptime(datetime_combined, '%Y-%m-%d %H:%M:%S.%f')
    end_datetime = start_datetime + timedelta(hours=float(service.duration))


    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    order = {
        'start_datetime': str(start_datetime),
        'end_datetime': str(end_datetime),
        'companion_selected': companion_selected,
    }

    # if bag has service in it already
    if service_name in list(bag.keys()):
        # loop through all orders with the same service name
        for x in bag[service_name]:
            # if the order has the same companion and datetime, fail
            if x['start_datetime'] == str(start_datetime) and x['companion_selected'] == companion_selected:
                print('already exists')
                messages.error(request, f'Already added "{service.name}" at this time to your bag')
                return redirect(redirect_url)
            # else add to existing orders list 
            else:
                print('matching service name, added new date/companion')
                bag[service_name].append(order)
                messages.success(request, f'Added "{service.name}" to your bag')
                request.session['bag'] = bag
                return redirect(redirect_url)
    # if bag does not have service in it already
    else:
        print('bag does not have service in it already')
        bag[service_name] = [order]
        messages.success(request, f'Added "{service.name}" to your bag')
        request.session['bag'] = bag
        return redirect(redirect_url)
    
    return redirect(redirect_url)

    # NEXT STEPS:
        # ensure the user can't add another of the same service name within the duration of the existing session
        # make sure date time html input is always capturing correct format, once had it fail
        # make sure stringifying the datetime object isn't going to cause issues, i think it's a string in the object that gets added to the database, so that will need to be converted back into a datetime object
        # ensure when checking out that the database holds the correct information about the order line items
        # allow user to adjust the date from bag, maybe this removes it and goes back to service detail with inputs prepopulated


# def adjust_bag(request, service_name):
#     """ Adjust quantity of the relevant service in the shopping bag """
#     # quantity = int(request.POST.get('quantity'))
#     # day_selected = request.POST.get('day', 'day_selected')
#     companion_selected = request.POST.get('companion', 'companion_selected')
#     bag = request.session.get('bag', {})

#     # for item in bag[service_name]:
#     #     if item['day_selected'] == day_selected and item['companion_selected'] == companion_selected:
#     #         item['quantity'] = quantity

#     messages.info(request, f'Updated "{service_name}" quantity to {quantity}')
#     request.session['bag'] = bag
#     return redirect(reverse('view_bag'))


def remove_from_bag(request, service_name):
    """ Remove item from the shopping bag """
    name = service_name.split("_")[0]
    start_datetime = service_name.split("_")[1]
    companion = service_name.split("_")[2]
    try:
        bag = request.session.get('bag', {})
        for item in bag[name]:
            if item['start_datetime'] == start_datetime and item['companion_selected'] == companion:
                deletion_index = bag[name].index(item)
                del bag[name][deletion_index]
        request.session['bag'] = bag
        messages.warning(request, f'Removed "{name}" from your bag')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'An error occured when attempting to remove "{service_name}" from your bag. Error code {e}')
        return HttpResponse(status=500)