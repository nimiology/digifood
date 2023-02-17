from django.contrib.auth import get_user_model
from django.db import models

from apps.food.models import Food


class Order(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=150, blank=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)


class OrderFood(models.Model):
    related_name = 'food_orders'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name=related_name)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name=related_name)
    count = models.PositiveIntegerField(default=1)
    instruction = models.CharField(max_length=300)
