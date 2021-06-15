from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from services.models import Service

def index(request):
	""" A view to return the index page """

	return render(request, 'home/index.html')

def search(request):
	""" A view to return the search page """

	services = Service.objects.all()
	query = None

	if request.GET:
		if 'q' in request.GET:
			query = request.GET['q']
			if not query:
				messages.error(request, "You didn't enter a search query")
				return redirect(reverse('home'))
			
			queries = Q(name__icontains=query)
			services = services.filter(queries)
	
	context = {
		'services': services,
		'search_term': query,
	}

	return render(request, 'home/search.html', context)