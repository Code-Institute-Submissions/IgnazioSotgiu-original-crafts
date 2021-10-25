"""
Admin panel settings
"""
from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    """
    Display reviews in the admin panel
    """
    readonly_fields = ('review_date',)

    fields = ('product', 'review_title', 'review_text', 'review_date',
              'author',)

    list_display = ('product', 'review_title', 'review_text',
                    'author',)

    ordering = ('-review_date',)


admin.site.register(Review, ReviewAdmin)
