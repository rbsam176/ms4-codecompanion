from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.profile, name='profile'),
    url(r'^ajax_pagination/$', views.ajax_pagination, name='ajax_pagination'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
