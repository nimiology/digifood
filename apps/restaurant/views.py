from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.food.views import FoodRatingListAPIView, FoodAPIView, FoodListAPIView, FoodRatingAPIView
from apps.restaurant.models import Restaurant, RestaurantRating
from apps.restaurant.serializers import RestaurantSerializer, RestaurantRatingSerializer


class RestaurantListAPIView(FoodListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_fields = {
        'title': ['contains'],
        'categories': ['contains'],
        'address': ['contains'],
    }


class RestaurantAPIView(FoodAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRatingListAPIView(FoodRatingListAPIView):
    queryset = RestaurantRating.objects.all()
    serializer_class = RestaurantRatingSerializer
    filterset_fields = {'owner': ['exact'],
                        'restaurant': ['exact'],
                        'rating': ['exact'],
                        'comment': ['contains'],
                        }


class RestaurantRatingAPIView(FoodRatingAPIView):
    serializer_class = RestaurantRatingSerializer

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Restaurant.objects.all()
        else:
            return RestaurantRating.objects.all()

    def destroy(self, request, *args, **kwargs):
        food = self.get_object()
        instance = get_object_or_404(RestaurantRating.objects.all(), restaurant=food, owner=self.request.user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
