from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Admin, MapUserToRole
from ..serializers import AdminSerializer

class UserAuthTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

        # Create an Admin object
        self.admin_data = {
            'first_name': 'Test',
            'last_name': 'Admin',
        }
        self.admin = Admin.objects.create(**self.admin_data)

        # Map user to Admin role
        self.mapping = MapUserToRole.objects.create(
            uuid=self.user.id,
            role=1,  # Assuming 1 is the role for Admin
            relatedid=self.admin.id
        )

    def test_login(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': self.user.username,
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['role']['user_type'], 1)  # Ensure user role is Admin

    def test_login_invalid_user(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'invaliduser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No User matches the given query.')

    def test_signup(self):
        url = reverse('signup')
        new_user_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'new@example.com'
        }
        response = self.client.post(url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_get_user_by_id(self):
        url = reverse('user_by_id', kwargs={'user_id': self.user.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_edit_user(self):
        url = reverse('edit_user')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, {
            'id': self.user.id,
            'username': 'updateduser',
            'password': 'updatedpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'updateduser')

    def test_delete_user(self):
        url = reverse('delete_user_by_id', kwargs={'user_id': self.user.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'User deleted successfully.')

    def test_token_verification(self):
        url = reverse('test_token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)

        # Check if the response data contains the entire string
        self.assertIn(f'passed for {self.user.username}', response.data)


