from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Organizer, MapUserToRole  # Adjust the import path according to your project structure
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..serializers import OrganizerSerializer  # Assuming you have a serializer for Organizer

User = get_user_model()

class OrganizerAPITests(APITestCase):
    def setUp(self):
        # Create a user and generate token for authentication
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create an organizer object
        self.organizer = Organizer.objects.create(
            first_name="Test",
            last_name="User",
            region="Test Region"
        )

        # Create a user-role mapping
        MapUserToRole.objects.create(uuid=self.user.id, role=2, relatedid=self.organizer.id)

    def get_auth_headers(self):
        return {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }

    def test_organizer_by_id(self):
        url = reverse('organizer_by_id', args=[self.organizer.id])
        response = self.client.get(url)
        expected_data = {"organizer": OrganizerSerializer(instance=self.organizer).data}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_organizer(self):
        url = reverse('create_organizer')
        data = {
            "first_name": "New",
            "last_name": "Organizer",
            "region": "New Region"
        }
        response = self.client.post(url, data, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['organizer']['first_name'], "New")

    def test_edit_organizer(self):
        url = reverse('edit_organizer')  # Pass the organizer ID
        data = {
            "id": self.organizer.id,  # Add the ID here
            "first_name": "Updated",
            "last_name": "User",
            "region": "Updated Region"
        }
        response = self.client.post(url, data, **self.get_auth_headers())  # Use the method
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['organizer']['first_name'], "Updated")

    def test_delete_organizer(self):
        url = reverse('delete_organizer', args=[self.organizer.id])
        response = self.client.delete(url, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Organizer deleted successfully.")
        self.assertFalse(Organizer.objects.filter(id=self.organizer.id).exists())
