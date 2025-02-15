from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ManyToManyField('Category')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    protein = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    carbonhydrates = models.FloatField(default=0)
    calories = models.FloatField(default=0)


    def __str__(self):
        result = ''
        categories = Category.objects.filter(item__name=self.name)
        for i, cat in enumerate(categories):
            result += f' {cat}{"," if i != len(categories)-1 else""}'
        return f'Product: {self.name} Category: {result}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)



    def __str__(self):
        return f'{self.name} /{self.url}/'


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Ожидает'), ('Shipped', 'Отправлено'), ('Delivered', 'Доставлено')],
        default='Pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.customer} - {self.total_price} - {self.created_date.date()} - {str(self.created_date.time())[:8]}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location_x = models.FloatField()
    location_y = models.FloatField()

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bonus = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username



class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Storage(models.Model):
    name = models.CharField(max_length=100, default='None')
    address = models.CharField(max_length=200, default='None')
    street = models.CharField(max_length=100, default='None')

    def __str__(self):
        return f'{self.name} - {self.address}'


class ItemsInStorage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.item} | Storage - {self.storage} | Amount - {self.stock}'

class ActivateCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    created_date = models.DateTimeField()

