from django.urls import path
from . import views

urlpatterns = [
    path('', views.active_sessions, name="active_sessions"),
]
