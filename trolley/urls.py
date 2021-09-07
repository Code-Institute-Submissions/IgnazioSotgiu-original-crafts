from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_trolley, name='view_trolley'),
    path('add/<product_id>', views.add_to_trolley, name='add_to_trolley'),
]