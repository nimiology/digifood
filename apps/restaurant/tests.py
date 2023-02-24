from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.restaurant.models import Restaurant, RestaurantRating
from apps.user.tests import get_user_token


class RestaurantAPITest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.restaurant = Restaurant.objects.create(title='restaurant', address='test')
        self.restaurant_rating = RestaurantRating.objects.create(owner=self.user, restaurant=self.restaurant,
                                                                 rating='4',)

    def test_create_restaurant(self):
        response = self.client.post(reverse('restaurant:restaurant'), data={
            'title': 'test',
            'address': 'test',
            'categories': ['a']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['categories'][0]['title'], 'a')
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_delete_restaurant(self):
        response = self.client.delete(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0)

    def test_delete_restaurant_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_get_restaurant(self):
        response = self.client.get(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.restaurant.pk)

    def test_create_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse('restaurant:restaurant'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.put(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_not_staff(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.patch(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        response = self.client.put(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}),
                                   data={'address': 'test',
                                         'title': 'test',
                                         'categories': ['w']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['categories'][0]['title'], 'w')

    def test_patch(self):
        response = self.client.patch(reverse('restaurant:restaurant', kwargs={'pk': self.restaurant.pk}), data={
            'categories': ['ti']})
        self.assertEqual(response.data['categories'], status.HTTP_401_UNAUTHORIZED)

    def test_get_all_restaurants(self):
        response = self.client.get(reverse('restaurant:restaurant'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_restaurant_rating_post(self):
        self.restaurant_rating.delete()
        response = self.client.post(reverse('restaurant:restaurant_rating'),
                                    data={'restaurant': self.restaurant.pk, 'rating': '5'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['restaurant']['rating'], 5)

    def test_restaurant_ratings_list(self):
        response = self.client.get(reverse('restaurant:restaurant_rating'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_restaurant_rating_get(self):
        response = self.client.get(reverse('restaurant:restaurant_rating', kwargs={'pk': self.restaurant_rating.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_rating_delete(self):
        response = self.client.delete(reverse('restaurant:restaurant_rating', kwargs={'pk': self.restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_rating_delete_not_found(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('restaurant:restaurant_rating', kwargs={'pk': self.restaurant_rating.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
