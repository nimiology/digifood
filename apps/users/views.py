from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.users.models import MyUser
from apps.users.serializers import MyUserSerializer


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