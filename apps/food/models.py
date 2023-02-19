from django.contrib.auth import get_user_model
from django.db import models

from apps.category.models import Category
from apps.food.utils import upload_file
from apps.restaurant.models import Restaurant


class Food(models.Model):
    related_name = 'foods'

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name=related_name)
    title = models.CharField(max_length=70)
    categories = models.ManyToManyField(Category, blank=True, related_name=related_name)
    price = models.IntegerField(default=0)
    delivery_time = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    calorie = models.IntegerField(default=0)
    wishlist = models.ManyToManyField(get_user_model(), blank=True, related_name='wishlist_food')
    image = models.ImageField(upload_to=upload_file, blank=True, null=True)
    food_image1 = models.ImageField(upload_to=upload_file, blank=True, null=True)
    food_image2 = models.ImageField(upload_to=upload_file, blank=True, null=True)
    food_image3 = models.ImageField(upload_to=upload_file, blank=True, null=True)
    food_image4 = models.ImageField(upload_to=upload_file, blank=True, null=True)
    food_image5 = models.ImageField(upload_to=upload_file, blank=True, null=True)

    def rating(self):
        ratings = self.food_ratings.all()
        sum = 0
        for rating in ratings:
            sum += int(rating.rating)
        count = ratings.count()
        if count == 0:
            return 0
        return sum / count


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
    rating = models.CharField(max_length=1, choices=rating_choices)
    comment = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'food')
