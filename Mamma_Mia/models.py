from django.contrib.auth.models import User
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50)


class Pizza(models.Model):
    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    CATEGORY_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Meat', 'Meat'),
    ]

    DOUGHT_CHOICES = [
        ('Thin', 'Thin'),
        ('Traditional', 'Traditional')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    dough_type = models.CharField(max_length=50, choices=DOUGHT_CHOICES)
    ingredients = models.ManyToManyField(Ingredient)


class Topping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    toppings = models.ManyToManyField(Topping)
    address = models.TextField()
    customer_phone = models.CharField(max_length=50, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True)
    quantity = models.IntegerField(blank=True, null=True)


class Idea(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

