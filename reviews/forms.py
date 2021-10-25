from django.forms import ModelForm
from .models import Review


class ReviewForm(ModelForm):
    """
    A form to create review
    """

    class Meta:
        model = Review
        fields = ['product', 'review_title', 'review_text', 'author']
