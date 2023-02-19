from django.contrib import admin

from apps.restaurant.models import RestaurantRating, Restaurant

admin.site.register(Restaurant)
admin.site.register(RestaurantRating)