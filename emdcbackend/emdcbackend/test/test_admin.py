from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Admin, MapUserToRole
from ..serializers import AdminSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AdminTests(APITestCase):

    def setUp(self):
        # Create a user and generate token for authentication
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create an admin object
        self.admin = Admin.objects.create(
            first_name="Test",
            last_name="User",
        )

        # Create a user-role mapping
        MapUserToRole.objects.create(uuid=self.user.id, role=1, relatedid=self.admin.id)

    def test_admin_by_id(self):
        url = reverse("admin_by_id", args=[self.admin.id])
        response = self.client.get(url)
        expected_data = {"Admin": AdminSerializer(instance=self.admin).data}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_admins_get_all(self):
        url = reverse("admins_get_all")
        response = self.client.get(url)
        expected_data = {"Admins": AdminSerializer(Admin.objects.all(), many=True).data}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_admin(self):
        url = reverse("create_admin")
        data = {
            "first_name": "New",
            "last_name": "Admin",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Admin"]["first_name"], "New")

    def test_edit_admin(self):
        url = reverse("edit_admin")
        data = {
            "id": self.admin.id,
            "first_name": "Updated",
            "last_name": "User",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Admin"]["first_name"], "Updated")

    def test_delete_admin(self):
        url = reverse("delete_admin", args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Detail"], "Admin deleted successfully.")
        self.assertFalse(Admin.objects.filter(id=self.admin.id).exists())
