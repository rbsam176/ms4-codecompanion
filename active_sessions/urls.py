from django.urls import path
from . import views

urlpatterns = [
    path('<order_number>/', views.active_sessions, name='active_sessions'),
    path('', views.redirect_services),
]
