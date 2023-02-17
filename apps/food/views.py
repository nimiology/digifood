from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.food.models import Food, FoodRating
from apps.food.serializers import FoodSerializer, FoodRatingSerializer


class FoodListAPIView(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filterset_fields = {'restaurant': ['exact'],
                        'title': ['contains'],
                        'categories': ['contains'],
                        'price': ['exact', 'gte', 'lte', 'lt', 'gt'],
                        'delivery_time': ['contains'],
                        'description': ['contains'],
                        'calorie': ['exact', 'gte', 'lte', 'lt', 'gt'],
                        'wishlist': ['contains'],
                        }

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodListAPIView, self).post(request, *args, **kwargs)


class FoodAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodAPIView, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodAPIView, self).patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodAPIView, self).delete(request, *args, **kwargs)


class FoodWishlistAPI(GenericAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile = request.user
        pk = kwargs['pk']
        food = get_object_or_404(Food, pk=pk)
        food_wishlist = food.wishlist.all()
        if profile in food_wishlist:
            food.wishlist.remove(profile)
        else:
            food.wishlist.add(profile)
        return Response(self.get_serializer(food).data)


class FoodRatingListAPIView(ListCreateAPIView):
    queryset = FoodRating.objects.all()
    serializer_class = FoodRatingSerializer
    filterset_fields = {'owner': ['exact'],
                        'food': ['exact'],
                        'rating': ['exact'],
                        'comment': ['comment'],
                        }

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super(FoodRatingListAPIView, self).post(request, *args, **kwargs)


class FoodRatingAPIView(RetrieveDestroyAPIView):
    queryset = FoodRating.objects.all()
    serializer_class = FoodRatingSerializer

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodRatingAPIView, self).delete(request, *args, **kwargs)
