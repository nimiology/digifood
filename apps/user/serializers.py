from rest_framework import serializers
from apps.user.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = '__all__'