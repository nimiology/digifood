from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.food.models import Food, FoodRating
from apps.restaurant.models import Restaurant
from apps.user.tests import get_user_token


class FoodAPITest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.restaurant = Restaurant.objects.create(title='restaurant', address='test')
        self.food = Food.objects.create(restaurant=self.restaurant, title='test',
                                        image='test')
        self.food_rating = FoodRating.objects.create(owner=self.user, food=self.food, rating='5')

    def test_create_food(self):
        response = self.client.post(reverse('food:food'), data={'restaurant': self.restaurant.pk,
                                                                'title': 'test',
                                                                'categories': ['a']})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['categories'][0]['title'], 'a')
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
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        response = self.client.put(reverse('food:food', kwargs={'pk': self.food.pk}),
                                   data={'restaurant': self.restaurant.pk,
                                         'title': 'test',
                                         'categories': ['w']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['categories'][0]['title'], 'w')

    def test_patch(self):
        response = self.client.patch(reverse('food:food', kwargs={'pk': self.food.pk}), data={
            'categories': ['ti']})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def test_food_rating_post(self):
        self.food_rating.delete()
        response = self.client.post(reverse('food:food_rating'), data={'food': self.food.pk, 'rating': '5'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['food']['rating'], 5)

    def test_food_ratings_list(self):
        response = self.client.get(reverse('food:food_rating'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_food_rating_get(self):
        response = self.client.get(reverse('food:food_rating', kwargs={'pk': self.food_rating.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_food_rating_delete(self):
        response = self.client.delete(reverse('food:food_rating', kwargs={'pk': self.food_rating.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_food_rating_delete_not_found(self):
        user, token = get_user_token('John2')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('food:food_rating', kwargs={'pk': self.food_rating.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


