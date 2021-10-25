from django import forms
from .models import Product


# Code taken form code institute lecture


class ProductForm(forms.ModelForm):

    class Meta:
        """
        A form to create the product
        """
        model = Product
        fields = ['image', 'name', 'price', 'category',
                  'description', 'special_price',
                  'number_in_stock', 'hide_product', 'on_special',
                  'hot_tag', 'original_tag', 'selling_fast_tag',
                  'add_to_popular_products', 'new_tag']

        image = forms.ImageField(required=False)
