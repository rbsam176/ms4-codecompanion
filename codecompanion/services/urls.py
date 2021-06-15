from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_services),
    path('compare-services', views.compare_services, name='compare_services'),
    path('<endpoint>', views.service_detail, name='service_detail'),
]
