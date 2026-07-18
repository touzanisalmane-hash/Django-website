from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Customizes how products appear in the Django admin panel.
    Superusers/staff can add, edit, and delete products here by default —
    this class only customizes the *display*, it doesn't restrict anything.
    """
    list_display = ('name', 'price', 'stock', 'created_at')
    list_editable = ('price', 'stock')  # allows editing price/stock directly from the list
    search_fields = ('name',)
    list_filter = ('created_at',)

    # These are already True by default for staff/superusers, but are kept
    # explicit here so it's clear the admin can fully manage products.
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
