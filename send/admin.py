"""
Admin panel settings
"""
from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('email_date', )

    fields = ('from_email', 'recipient_list', 'email_subject',
              'message', 'email_date',)

    list_display = ('from_email', 'recipient_list', 'email_subject',
                    'message', 'email_date',)

    ordering = ('-email_date',)


admin.site.register(Contact, ContactAdmin)
