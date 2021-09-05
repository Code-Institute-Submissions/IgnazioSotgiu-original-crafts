from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_homepage, name='home'),
    path('store/', views.products, name='products'),
    path('<int:product_id>/', views.single_product, name='single_product'),
    path('search/', views.search_result, name='search_result'),
]
