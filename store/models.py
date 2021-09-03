from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=254, blank=False, null=False)
    friendly_name = models.CharField(max_length=254, blank=True, null=True)
    slug = models.SlugField(max_length=254, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product',
                                 on_delete=models.PROTECT, null=False,
                                 blank=False)
    name = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=4, decimal_places=2, null=False, blank=False)
    special_price = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number_in_stock = models.IntegerField(
            validators=[
                MinValueValidator(0),
                MaxValueValidator(100)
            ],
            default=99)
    hide_product = models.BooleanField(default=False)
    on_special = models.BooleanField(default=False)
    hot_tag = models.BooleanField(default=False)
    original_tag = models.BooleanField(default=False)
    selling_fast_tag = models.BooleanField(default=False)
    add_to_popular_products = models.BooleanField(default=True)
    new_tag = models.BooleanField(default=False)
    rating = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.name
