from django import forms
from .models import Product, Category


# Code taken form code institute lecture


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['image', 'name', 'price', 'category',
                  'description', 'special_price',
                  'number_in_stock', 'hide_product', 'on_special',
                  'hot_tag', 'original_tag', 'selling_fast_tag',
                  'add_to_popular_products', 'new_tag']

        image = forms.ImageField(required=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            categories = Category.objects.all()

            self.fields['category'].choices = categories
