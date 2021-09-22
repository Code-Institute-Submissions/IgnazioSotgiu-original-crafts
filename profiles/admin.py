from django.contrib import admin
from .models import Profiles

# Register your models here.


class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'street_address', 'town_or_city',
                    'county', 'country']


admin.site.register(Profiles, ProfilesAdmin)
