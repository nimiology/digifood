from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import MyUser


def get_user_token(username, is_staff=False):
    user = MyUser.objects.create(username=username, password='1234', is_staff=is_staff)
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'


class UserSearchTest(APITestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username='John', first_name='John', last_name='Doe',
                                               email='test@test.com', password='test')

    def test_user_search(self):
        response = self.client.get(reverse('user:search'), {'first_name': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')


class GetUserTest(APITestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username='John', first_name='John', last_name='Doe',
                                               email='test@test.com', password='test')

    def test_get_user(self):
        response = self.client.get(reverse('user:get', kwargs={'username': 'John'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'John')

    def test_get_user_not_found(self):
        response = self.client.get(reverse('user:get', kwargs={'username': 'John2'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)