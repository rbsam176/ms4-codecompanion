from django.shortcuts import render

# Create your views here.
def redirect_services(request):
	return redirect('/services/compare-services')