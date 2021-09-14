from django.contrib import admin
from .models import CheckoutOrder

# code from code institute lecture


class CheckoutOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'order_date', 'delivery',
                       'order_total', 'grand_total')

    fields = ('order_number', 'deliver_to_name', 'buyer_name',
              'email_address', 'town_or_city', 'county', 'country',
              'zip_postcode', 'order_date', 'delivery', 'order_total',
              'grand_total',)

    list_display = ('order_number', 'deliver_to_name', 'buyer_name',
                    'email_address', 'order_date', 'grand_total',)

    ordering = ('-order_date',)


admin.site.register(CheckoutOrder, CheckoutOrderAdmin)
