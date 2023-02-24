from django.urls import path

from apps.restaurant.views import RestaurantRatingAPIView, RestaurantRatingListAPIView, RestaurantListAPIView, \
    RestaurantAPIView

app_name = 'restaurant'
urlpatterns = [
    path('', RestaurantListAPIView.as_view(), name='restaurant'),
    path('<int:pk>/', RestaurantAPIView.as_view(), name='restaurant'),

    path('rating/', RestaurantRatingListAPIView.as_view(), name='restaurant_rating'),
    path('rating/<int:pk>/', RestaurantRatingAPIView.as_view(), name='restaurant_rating'),
]