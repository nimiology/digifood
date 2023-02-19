from django.contrib import admin

from apps.food.models import Food, FoodRating

admin.site.register(Food)
admin.site.register(FoodRating)