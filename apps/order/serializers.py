from rest_framework import serializers

from apps.food.serializers import FoodSerializer
from apps.order.models import Order, OrderFood
from apps.user.serializers import MyUserSerializer


class OrderSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ' __all__'


class OrderFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFood
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['order'] = OrderSerializer(read_only=True)
        self.fields['food'] = FoodSerializer(read_only=True)
        return super(OrderFoodSerializer, self).to_representation(instance)
