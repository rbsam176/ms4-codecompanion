from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_controls, name='admin_controls'),
    path('edit_question/', views.redirect_services),
    path('edit_question/<question_id>/', views.edit_question, name='edit_question'),
]
