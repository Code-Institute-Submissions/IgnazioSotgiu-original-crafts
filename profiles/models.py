from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    street_address = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=25, null=True, blank=True)
    zip_postcode = models.CharField(max_length=20, null=True, blank=True)
    county = models.CharField(max_length=30, null=True, blank=True)
    country = CountryField(
        blank_label='(select country)', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    # create a new user profile or updating an existing one
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
