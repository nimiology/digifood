from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.food.models import Food
from apps.order.models import Order, OrderFood
from apps.restaurant.models import Restaurant
from apps.user.tests import get_user_token


class OrderAPITest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.restaurant = Restaurant.objects.create(title='restaurant', address='test')
        self.food = Food.objects.create(restaurant=self.restaurant, title='test',
                                        image='test')
        self.order = Order.objects.create(owner=self.user)
        self.order_food = OrderFood.objects.create(order=self.order, food=self.food)

    def test_get_all_orders(self):
        response = self.client.get(reverse('order:order'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Order.objects.count())

    def test_get_all_orders_is_staff(self):
        user, token = get_user_token('Jane', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Order.objects.count())

    def test_get_all_orders_no_one(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_post_order(self):
        response = self.client.post(reverse('order:order'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(reverse('order:order'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_not_owner(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_is_staff(self):
        user, token = get_user_token('Steve', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order(self):
        response = self.client.get(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_not_owner(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_is_staff(self):
        user, token = get_user_token('Steve', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order(self):
        response = self.client.delete(reverse('order:order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_order_foods(self):
        response = self.client.get(reverse('order:order_food'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], OrderFood.objects.count())

    def test_get_all_order_foods_is_staff(self):
        user, token = get_user_token('Jane', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order_food'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], OrderFood.objects.count())

    def test_get_all_order_foods_no_one(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order_food'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_post_order_food(self):
        response = self.client.post(reverse('order:order_food'), data={'order': self.order.pk, 'food': self.food.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_food_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(reverse('order:order_food'), data={'order': self.order.pk, 'food': self.food.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_food_not_owner(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_food_is_staff(self):
        user, token = get_user_token('Steve', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_food(self):
        response = self.client.get(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_food_not_owner(self):
        user, token = get_user_token('Steve')
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_food_is_staff(self):
        user, token = get_user_token('Steve', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.delete(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_food(self):
        response = self.client.delete(reverse('order:order_food', kwargs={'pk': self.order_food.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
