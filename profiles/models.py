from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profiles(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    street_address = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=25, null=True, blank=True)
    zip_postcode = models.CharField(max_length=20, null=True, blank=True)
    county = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name
        
