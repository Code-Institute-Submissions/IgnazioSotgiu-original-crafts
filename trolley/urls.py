from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_trolley, name='view_trolley'),
    path('add/<product_id>/', views.add_to_trolley, name='add_to_trolley'),
    path('update/<product_id>/', views.update_trolley, name='update_trolley'),
    path('delete/<product_id>/',
         views.delete_trolley_product, name='delete_trolley_product'),
]
