from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Shows order items inside the order's own page in the admin panel.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Shows orders in the admin panel, with the ability to view their details.
    """
    list_display = ('id', 'user', 'total_price', 'created_at')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]
