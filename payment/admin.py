from django.contrib import admin
from .models import ShippingAdrress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAdrress)
admin.site.register(Order)
admin.site.register(OrderItem)

#crear on orden item inline
class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

#extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInLine]

#registrar
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
