from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    path('', views.faq, name='faq'),
    path('add', views.add_faq, name='add_faq'),
    url(r'^counter/$', views.faq_counter, name='faq_counter'),
]
