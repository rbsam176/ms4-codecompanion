from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.
def view_bag(request):
	""" A view to return the shopping bag """

	return render(request, 'bag/bag.html')

def add_to_bag(request, service_name):
    """ Add a quantity of the clicked service to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if service_name in list(bag.keys()):
        bag[service_name] += quantity
    else:
        bag[service_name] = quantity
    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def adjust_bag(request, service_name):
    """ Adjust quantity of the relevant service in the shopping bag """
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})
    bag[service_name] = quantity
    
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, service_name):
    """ Remove item from the shopping bag """
    try:
        bag = request.session.get('bag', {})
        bag.pop(service_name)
        
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)