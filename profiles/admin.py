from django.contrib import admin
from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'town_or_city',
                    'county', 'country']


admin.site.register(Profile, ProfileAdmin)
