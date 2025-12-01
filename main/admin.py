from django.contrib import admin
from .models import Category, Cart, Product, CartItem, OrderItem, Order

# Register your models here.

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
