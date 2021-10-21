from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='rewiews')
    review_title = models.CharField(max_length=254, null=False, blank=False)
    review_text = models.TextField(max_length=1024, null=False, blank=False)
    review_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='user_reviews')

    def __str__(self):
        return self.review_title
