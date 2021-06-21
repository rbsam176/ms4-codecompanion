from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_services),
    path('compare-services/', views.compare_services, name='compare_services'),
    path('add/', views.add_service, name='add_service'),
    path('edit/<endpoint>/', views.edit_service, name='edit_service'),
    path('delete/<endpoint>/', views.delete_service, name='delete_service'),
    path('<endpoint>/', views.service_detail, name='service_detail'),

]
