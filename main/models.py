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

    def __str__(self):
        result = ''
        categories = Category.objects.filter(item__name=self.name)
        for i, cat in enumerate(categories):
            result += f' {cat}{"," if i != len(categories)-1 else""}'
        return f'Product: {self.name} Category: {result}'


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    created_data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Ожидает'), ('Shipped', 'Отправлено'), ('Delivered', 'Доставлено')],
        default='Pending'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
