from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.category.models import Category
from apps.food.models import Food
from apps.restaurant.models import Restaurant
from apps.user.tests import get_user_token


class RePostAPITest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.restaurant = Restaurant.objects.create(title='restaurant', address='test')
        self.food = Food.objects.create(restaurant=self.restaurant, title='test',
                                        image='test')

    def test_create_food(self):
        response = self.client.post(reverse('food:food'), data={'restaurant': self.restaurant.pk,
                                                                'title': 'test',
                                                                'categories': ['a']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['categories'][0]['title'], 'a')
        self.assertEqual(response.data['rating'], 0)
        self.assertEqual(Food.objects.count(), 2)

    def test_delete_food(self):
        response = self.client.delete(reverse('food:food', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Food.objects.count(), 0)

    def test_delete_food_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('food:food', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Food.objects.count(), 1)

    def test_get_food(self):
        response = self.client.get(reverse('food:food', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.food.pk)

    def test_create_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse('food:food'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('food:food', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('food:food', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        response = self.client.put(reverse('food:food', kwargs={'pk': self.food.pk}),
                                   data={'restaurant': self.restaurant.pk,
                                         'title': 'test',
                                         'categories': ['w']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['categories'][0]['title'], 'w')

    def test_patch(self):
        response = self.client.patch(reverse('food:food', kwargs={'pk': self.food.pk}),data={
                                         'categories': ['ti']})
        self.assertEqual(response.data['categories'], status.HTTP_401_UNAUTHORIZED)

    def test_get_all_foods(self):
        response = self.client.get(reverse('food:food'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_wishlist(self):
        response = self.client.post(reverse('food:food_wishlist', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['wishlist'][0], self.user.username)
        response = self.client.post(reverse('food:food_wishlist', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['wishlist']), 0)
