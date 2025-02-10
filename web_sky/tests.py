from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User
from web_sky.models import Course


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.url_create = reverse('web_sky:lessons-create')
        self.url_list = reverse('web_sky:lessons')
        self.data_create = {"name": "Тесты", "lesson_link": "https://www.youtube.com/watch?v=BMZNqftgTC8"}

    def test_post(self):
        response = self.client.post(self.url_create, self.data_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='testcourse')
        self.url = reverse('web_sky:subscription')
        self.data = {"course_id": 1}

    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
