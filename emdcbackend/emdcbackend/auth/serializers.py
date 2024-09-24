from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'userType']  # Django auth requires at least a username and password field
                                                             # Use username field for email addresses
