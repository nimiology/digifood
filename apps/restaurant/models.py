from django.contrib.auth import get_user_model
from django.db import models

from apps.category.models import Category


class Restaurant(models.Model):
    title = models.CharField(max_length=70)
    address = models.CharField(max_length=300)
    category = models.ManyToManyField(Category, blank=True, related_name='restaurant')
    image = models.ImageField(blank=True, null=True)

    def rating(self):
        ratings = self.restaurant_ratings.all()
        sum = 0
        for rating in ratings:
            sum += int(rating.rating)
        return sum / ratings.count()


class RestaurantRating(models.Model):
    related_name = 'restaurant_ratings'

    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name=related_name)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name=related_name)
    rating = models.CharField(choices=rating_choices)
    comment = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        unique_together = ('owner', 'restaurant')
