from django.contrib import admin
from .models import CheckoutOrder, OrderLineItem

# code from code institute lecture


class CheckoutOrderLineItemAdmin(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class CheckoutOrderAdmin(admin.ModelAdmin):
    inlines = (CheckoutOrderLineItemAdmin,)
    readonly_fields = ('order_number', 'order_date', 'delivery',
                       'order_total', 'grand_total', 'order_pid')

    fields = ('order_number', 'full_name',
              'email_address', 'town_or_city', 'county', 'country',
              'zip_postcode', 'order_date', 'delivery', 'order_total',
              'grand_total', 'order_trolley', 'order_pid',)

    list_display = ('order_number', 'full_name',
                    'email_address', 'order_date', 'grand_total',)

    ordering = ('-order_date',)


admin.site.register(CheckoutOrder, CheckoutOrderAdmin)
