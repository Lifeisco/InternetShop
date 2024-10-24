from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField()  # Описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара A.BC
    stock = models.PositiveIntegerField()  # Количество товаров на складе
    category = models.ManyToManyField('Category')  # Категория товара TODO manytomany
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Изображение товара
    created_date = models.DateTimeField(auto_now_add=True)  # Время создания записи
    updated_date = models.DateTimeField(auto_now=True)  # Время последнего обновления

    def __str__(self):
        return f'Product: {self.name} Category: {self.category.name}'


class Category(models.Model):
    name = models.CharField(max_length=255)  # Название категории


    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)  # Покупатель
    created_data = models.DateTimeField(auto_now_add=True)  # Время создания заказа
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Ожидает'), ('Shipped', 'Отправлено'), ('Delivered', 'Доставлено')],
        default='Pending'
    )  # Статус заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая сумма заказа


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Заказ
    product = models.ForeignKey(Item, on_delete=models.CASCADE)  # Товар
    quantity = models.PositiveIntegerField()  # Количество товаров
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Ccылка на User
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)  # Ccылка на Item
    price_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)  # Ссылка на общую цену
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
