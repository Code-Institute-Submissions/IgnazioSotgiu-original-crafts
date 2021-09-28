"""
Admin panel settings
"""
from django.contrib import admin
from .models import Review

# code from code institute lecture


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('review_date',)

    fields = ('product', 'review_title', 'review_text', 'review_date',
              'author',)

    list_display = ('product', 'review_title', 'review_text',
                    'author',)

    ordering = ('-review_date',)


admin.site.register(Review, ReviewAdmin)
