from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# mejorar profile info y info user

class ProfileInLine(admin.StackedInline):
    model = Profile

# extender modelo  de usuario

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)