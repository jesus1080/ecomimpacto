from django.contrib import admin
from .models import ShippingAdrress, Order, OrderItem

# Register your models here.
admin.site.register(ShippingAdrress)
admin.site.register(Order)
admin.site.register(OrderItem)
