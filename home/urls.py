from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('search', views.search, name="search"),
    path('companions/', views.companions, name="companions"),
]
