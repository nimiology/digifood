from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.category.models import Category
from apps.user.tests import get_user_token


class CategoryAPITest(APITestCase):
    def setUp(self) -> None:
        self.user, self.token = get_user_token('John', is_staff=True)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.category = Category.objects.create(title='test')

    def test_category_post(self):
        response = self.client.post(reverse('category:category'), data={'title': 'test25'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_not_staff(self):
        self.user, self.token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(reverse('category:category'), data={'title': 'test25'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_get(self):
        response = self.client.get(reverse('category:category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Category.objects.count())

    def test_category_delete(self):
        response = self.client.delete(reverse('category:category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_delete_not_staff(self):
        self.user, self.token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(reverse('category:category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_get(self):
        self.user, self.token = get_user_token('Jane')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(reverse('category:category', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
