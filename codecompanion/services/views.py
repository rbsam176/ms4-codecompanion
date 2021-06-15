from django.shortcuts import render, redirect

def redirect_services(request):
	return redirect('/services/compare-services')

def compare_services(request):
	""" A view to return the Compare Services page """

	return render(request, 'services/compare_services.html')