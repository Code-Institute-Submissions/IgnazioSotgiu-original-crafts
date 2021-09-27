from django.urls import path
from . import views

urlpatterns = [
     path('profiles/', views.profile_page, name='profile_page'),
     path('profiles/ profile_order_history/<order_number>/',
          views.profile_order_history, name='profile_order_history'),
]
