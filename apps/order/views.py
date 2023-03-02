from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.order.models import Order, OrderFood
from apps.order.serializers import OrderSerializer, OrderFoodSerializer


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer
    filterset_fields = {
        'owner': ['exact'],
        'address': ['contains'],
        'paid': ['exact'],
        'delivered': ['exact'],
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super(OrderListCreateAPIView, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class OrderAPIView(RetrieveDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=self.request.user)


class OrderFoodListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderFoodSerializer
    filterset_fields = {
        'order': ['exact'],
        'count': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'food': ['exact'],
        'instruction': ['contains'],
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderFood.objects.all()
        return OrderFood.objects.filter(order__owner=self.request.user)

    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super(OrderFoodListCreateAPIView, self).post(request, *args, **kwargs)


class OrderFoodAPIView(RetrieveDestroyAPIView):
    serializer_class = OrderFoodSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderFood.objects.all()
        return OrderFood.objects.filter(order__owner=self.request.user)
