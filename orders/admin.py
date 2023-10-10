from django.contrib import admin

from .models import Order, OrderItem


class ItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'data_created']
    inlines = [ItemInline, ]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
