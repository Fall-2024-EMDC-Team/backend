from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ...models import MapUserToRole, Coach, Organizer
from ...serializers import MapUserToRoleSerializer, UserSerializer, CoachSerializer, OrganizerSerializer
# TO-DO: Add Admin to This

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_role_mapping(request,role):
  # role should map directly to the ENUM Found in Role Enum, Line 49 in Models.py
  if role == 1:
    return Request("ERROR: Admin user role not implemented yet!", status=status.HTTP_400_BAD_REQUEST)
  else:
    serializer = MapUserToRoleSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"mapping": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_coach_by_user(request,userid):
  


