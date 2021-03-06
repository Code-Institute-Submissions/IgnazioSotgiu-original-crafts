from django.urls import path
from . import views

urlpatterns = [
     path('reviews/add_review/<int:product_id>/',
          views.add_review, name='add_review'),
     path('reviews/edit_review/<int:review_id>/',
          views.edit_review, name='edit_review'),
     path('reviews/delete_review_warning/<int:review_id>/',
          views.delete_review_warning, name='delete_review_warning'),
     path('reviews/delete_review/<int:review_id>/',
          views.delete_review, name='delete_review'),
]
