from django.contrib import admin
from main.models import Item, Category, ShoppingCart, Order

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(ShoppingCart)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ["status"]
