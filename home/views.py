from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from services.models import Service
from faq.models import FaqEntry
from profiles.models import CompanionProfile


def index(request):
    """ A view to return the index page and top 4 faq """
    faq_ordered = (
        FaqEntry.objects.all()
        .order_by("-clickCount")
        .values("clickCount", "title", "content")[:4]
    )

    context = {
        "faq_ordered": faq_ordered,
    }
    return render(request, "home/index.html", context)


def search(request):
    """ A view to return the search page """

    services = Service.objects.all()
    companions = CompanionProfile.objects.all()
    query = None

    if request.GET:
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter a search query")
                return redirect(reverse("home"))

            services_query = Q(name__icontains=query)
            services_results = services.filter(services_query)

            companions_query = Q(user__username__icontains=query)
            companions_results = companions.filter(companions_query)

    context = {
        "search_term": query,
        "services_results": services_results,
        "companions_results": companions_results,
    }

    return render(request, "home/search.html", context)


def companions(request):
    """ A view to return the list of companions page """
    companions = CompanionProfile.objects.all()

    context = {
        "companions": companions,
    }

    return render(request, "home/companions.html", context)
