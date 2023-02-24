from rest_framework import serializers

from apps.category.models import Category
from apps.category.serializers import CategorySerializer
from apps.restaurant.models import Restaurant, RestaurantRating
from apps.user.serializers import MyUserSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'title',
            'address',
            'categories',
            'image',
            'rating',
        ]

    def to_internal_value(self, data):
        if 'categories' in data:
            for category in data['categories']:
                Category.objects.get_or_create(title=category)
        return super(RestaurantSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        self.fields['categories'] = CategorySerializer(many=True)
        return super(RestaurantSerializer, self).to_representation(instance)


class RestaurantRatingSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True)

    class Meta:
        model = RestaurantRating
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['restaurant'] = RestaurantSerializer(read_only=True)
        return super(RestaurantRatingSerializer, self).to_representation(instance)
