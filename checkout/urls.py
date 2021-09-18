from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_checkout_page, name='view_checkout_page'),
    path('checkout_completed/<order_number>', views.checkout_completed, name='checkout_completed'),
]
