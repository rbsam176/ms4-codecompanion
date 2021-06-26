from django.shortcuts import get_object_or_404, render, redirect, reverse, HttpResponse
from django.contrib import messages

from services.models import Service

# Create your views here.
def view_bag(request):
	""" A view to return the shopping bag """

	return render(request, 'bag/bag.html')

def add_to_bag(request, service_name):
    """ Add a quantity of the clicked service to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    day_selected = request.POST.get('daySelection')
    companion_selected = request.POST.get('companionSelection')

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    service = Service.objects.get(pk=service_name)

    # if bag has service in it already
    if service_name in list(bag.keys()):
        already_exists = False
        # for every bag entry of this service
        for x in bag[service_name]:
            # if bag entry has the same day and companion selected
            if x['day_selected'] == day_selected and x['companion_selected'] == companion_selected:
                # increment the quantity
                x['quantity'] += 1
                # mark as it already existing in the bag
                already_exists = True

        order = {
            'quantity': quantity,
            'day_selected': day_selected,
            'companion_selected': companion_selected,
        }
        
        # if bag has service in it but not the same day/companion
        if already_exists == False:
            # add to bag dict
            bag[service_name].append(order)

        messages.success(request, f'Added "{service.name}" to your bag')
    else:
        order = {
            'quantity': quantity,
            'day_selected': day_selected,
            'companion_selected': companion_selected,
        }
        bag[service_name] = [order]
        messages.success(request, f'Added "{service.name}" to your bag')
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, service_name):
    """ Adjust quantity of the relevant service in the shopping bag """
    quantity = int(request.POST.get('quantity'))
    day_selected = request.POST.get('day', 'day_selected')
    companion_selected = request.POST.get('companion', 'companion_selected')
    bag = request.session.get('bag', {})

    for item in bag[service_name]:
        if item['day_selected'] == day_selected and item['companion_selected'] == companion_selected:
            item['quantity'] = quantity

    messages.info(request, f'Updated "{service_name}" quantity to {quantity}')
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, service_name):
    """ Remove item from the shopping bag """
    name = service_name.split("_")[0]
    day = service_name.split("_")[1]
    companion = service_name.split("_")[2]
    try:
        bag = request.session.get('bag', {})
        for item in bag[name]:
            if item['day_selected'] == day and item['companion_selected'] == companion:
                print(item)
                deletion_index = bag[name].index(item)
                del bag[name][deletion_index]
        request.session['bag'] = bag
        messages.warning(request, f'Removed "{name}" from your bag')
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'An error occured when attempting to remove "{service_name}" from your bag. Error code {e}')
        return HttpResponse(status=500)