from django.contrib.auth import get_user_model
from django.db import models


class Restaurant(models.Model):
    title = models.CharField(max_length=70)
    address = models.CharField(max_length=300)
    image = models.ImageField(blank=True, null=True)


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
