from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField
import uuid
from django.conf import settings
from store.models import Product

# code taken from code institute lecture


class CheckoutOrder(models.Model):
    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=60, null=False, blank=False)
    email_address = models.EmailField(max_length=254, null=False, blank=False)
    street_address = models.CharField(max_length=254, null=False, blank=False)
    town_or_city = models.CharField(max_length=254, null=False, blank=False)
    county = models.CharField(max_length=254, null=True, blank=True)
    country = CountryField(
        blank_label='(select country)', null=False, blank=False)
    zip_postcode = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(
        max_digits=4, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, default=0)
    order_trolley = models.TextField(
        null=False, blank=False, default='')
    order_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    # Create an order number
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    # Check if there is a order number if not call the function to create it
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum(
            'lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_MIN_SPEND:
            self.delivery = self.order_total * settings.APPLY_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery = 0

        self.grand_total = self.order_total + self.delivery
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        CheckoutOrder, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False,
        blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        if self.product.special_price:
            self.lineitem_total = self.product.special_price * self.quantity
        else:
            self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Product: {self.product.name} -\
            order {self.order.order_number}'
