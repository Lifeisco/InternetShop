from django.contrib import admin
from main.models import Item, Category, ShoppingCart, Order, Courier, Customer, Storage, ItemsInStorage

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(ShoppingCart)
admin.site.register(Courier)
admin.site.register(Customer)
admin.site.register(Storage)
admin.site.register(ItemsInStorage)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ["status"]
