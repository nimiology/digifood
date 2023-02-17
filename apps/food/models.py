from django.contrib.auth import get_user_model
from django.db import models

from apps.category.models import Category
from apps.food.utils import upload_file


class Food(models.Model):
    title = models.CharField(max_length=70)
    category = models.ManyToManyField(Category, blank=True, related_name='foods')
    price = models.IntegerField(default=0)
    delivery_time = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    calorie = models.IntegerField(default=0)
    wishlist = models.ManyToManyField(get_user_model(), blank=True, related_name='wishlist_food')
    image = models.ImageField(upload_to=upload_file)
    food_image1 = models.ImageField(upload_to=upload_file)
    food_image2 = models.ImageField(upload_to=upload_file)
    food_image3 = models.ImageField(upload_to=upload_file)
    food_image4 = models.ImageField(upload_to=upload_file)
    food_image5 = models.ImageField(upload_to=upload_file)


class FoodRating(models.Model):
    related_name = 'food_ratings'

    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=related_name)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name=related_name)
    rating = models.CharField(choices=rating_choices)
    comment = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'food')

