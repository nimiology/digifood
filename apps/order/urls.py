from django.urls import path

from apps.order.views import OrderListCreateAPIView, OrderAPIView, OrderFoodListCreateAPIView, OrderFoodAPIView

app_name = 'order'

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order'),
    path('<int:pk>/', OrderAPIView.as_view(), name='order'),

    path('food/', OrderFoodListCreateAPIView.as_view(), name='order_food'),
    path('food/<int:pk>/', OrderFoodAPIView.as_view(), name='order_food'),
]