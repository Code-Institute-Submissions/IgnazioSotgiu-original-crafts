from django.urls import path
from . import views

urlpatterns = [
     path('send/send_email/',
          views.send_email, name='send_email'),
]
