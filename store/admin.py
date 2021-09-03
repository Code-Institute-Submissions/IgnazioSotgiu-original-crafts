from django.contrib import admin

from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'friendly_name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price',
                    'special_price', 'number_in_stock']
    list_filter = ['created', 'number_in_stock', 'updated',
                   'name']
    ordering = ('-created',)


admin.site.register(Product, ProductAdmin)
