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
    queryset = Food.objects.all()
    serializer_class = FoodRatingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        food = get_object_or_404(queryset, **filter_kwargs)
        obj = get_object_or_404(FoodRating.objects.all(), owner=self.request.user, food=food)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super(FoodRatingAPIView, self).delete(request, *args, **kwargs)
