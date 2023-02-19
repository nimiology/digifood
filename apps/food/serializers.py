from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from apps.category.models import Category
from apps.category.serializers import CategorySerializer
from apps.food.models import Food, FoodRating
from apps.user.serializers import MyUserSerializer


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
            'restaurant',
            'title',
            'categories',
            'price',
            'delivery_time',
            'description',
            'calorie',
            'wishlist',
            'image',
            'food_image1',
            'food_image2',
            'food_image3',
            'food_image4',
            'food_image5',
            'rating',
        ]

    def to_internal_value(self, data):
        if 'categories' in data:
            for category in data['categories']:
                Category.objects.get_or_create(title=category)
        return super(FoodSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        self.fields['categories'] = CategorySerializer(many=True)
        self.fields['wishlist'] = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)
        return super(FoodSerializer, self).to_representation(instance)



class FoodRatingSerializer(serializers.ModelSerializer):
    owner = MyUserSerializer(read_only=True)

    class Meta:
        model = FoodRating
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['food'] = FoodSerializer(read_only=True)
        return super(FoodRatingSerializer, self).to_representation(instance)
