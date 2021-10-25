from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Display profile data in the admin panel
    """
    list_display = ['user', 'street_address', 'town_or_city',
                    'county', 'country']


admin.site.register(Profile, ProfileAdmin)
