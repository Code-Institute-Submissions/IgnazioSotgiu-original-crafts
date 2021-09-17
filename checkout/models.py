from django.db import models
from django_countries.fields import CountryField
import uuid
from django.conf import settings

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

    def calculate_delivery_cost(self):
        if self.order_total < settings.FREE_DELIVERY_MIN_SPEND:
            self.delivery = self.order_total * (
                settings.FREE_DELIVERY_MIN_SPEND / 100)
        else:
            self.delivery = 0

        self.grand_total = self.order_total + self.delivery
        self.save()

    # Create an order number
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    # Check if order number exsists, if not create one
    def save(self, *args, **kwargs):
        """
        Make sure the order number has been created.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
