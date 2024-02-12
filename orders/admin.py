from django.contrib import admin

from .models import Order, OrderItem


class ItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'color', 'size', 'price', ]
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user', 'is_paid', 'date_time_created']
    inlines = [ItemInline, ]


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ['order', 'product', 'quantity', 'price']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
