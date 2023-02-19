from django.urls import path

from apps.food.views import FoodListAPIView, FoodAPIView, FoodWishlistAPI, FoodRatingListAPIView, FoodRatingAPIView

app_name = 'food'
urlpatterns = [
    path('', FoodListAPIView.as_view(), name='food'),
    path('<int:pk>/', FoodAPIView.as_view(), name='food'),

    path('<int:pk>/wishlist/', FoodWishlistAPI.as_view(), name='food_wishlist'),

    path('rating/', FoodRatingListAPIView.as_view(), name='food_rating'),
    path('rating/<int:pk>/', FoodRatingAPIView.as_view(), name='food_rating'),
]