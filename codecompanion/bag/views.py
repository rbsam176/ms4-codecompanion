from django.shortcuts import render, redirect

# Create your views here.
def view_bag(request):
	""" A view to return the shopping bag """

	return render(request, 'bag/bag.html')

def add_to_bag(request, service_name):
    """ Add a quantity of the clicked product to the shopping bag """
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