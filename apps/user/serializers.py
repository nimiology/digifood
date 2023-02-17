from rest_framework import serializers
from apps.user.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'timezone',
                  ]