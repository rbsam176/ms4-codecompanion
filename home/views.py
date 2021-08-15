from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from services.models import Service
from faq.models import FaqEntry
from profiles.models import CompanionProfile

def index(request):
	""" A view to return the index page and top 4 faq """
	faq_ordered = FaqEntry.objects.all().order_by('-clickCount').values('clickCount', 'title', 'content')[:4]
	context = {
		'faq_ordered': faq_ordered,
	}
	return render(request, 'home/index.html', context)


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


def companions(request):
	""" A view to return the list of companions page """
	companions = CompanionProfile.objects.all()

	context = {
	'companions': companions,
	}

	return render(request, 'home/companions.html', context)