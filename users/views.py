import pytz
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, get_object_or_404, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import MyUser
from users.serializers import MyUserSerializer


class UserSearch(ListAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    filterset_fields = {'first_name': ['contains'],
                        'username': ['contains'],
                        }


class GetUser(RetrieveAPIView):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    lookup_field = 'username'