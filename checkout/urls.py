from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_checkout_page, name='view_checkout_page'),
]
