from django.urls import path
from . import views

urlpatterns = [
     path('', views.profile_page, name='profile_page'),
     path('profile_order_history/<order_number>/',
          views.profile_order_history, name='profile_order_history'),
]
