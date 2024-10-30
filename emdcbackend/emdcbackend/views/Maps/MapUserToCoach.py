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

from ...models import MapUserToCoach, Coach, User
from ...serializers import MapUserToCoachSerializer, CoachSerializer, UserSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_Coach_mapping(request):
  serializer = MapUserToCoachSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response({"mapping": serializer.data}, status=status.HTTP_201_CREATED)
  else:
    return Response(
      serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_Coach_by_user_id(request, uuid_id):
  Coach_ids = MapUserToCoach.objects.filter(request.data["id"])
  Coachs = Coach.objects.filter(id__in=Coach_ids)
  serializer = CoachSerializer(Coachs, many=True)
  return Response({"Coachs":serializer.data()},status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_Coach_id(request,Coach_id):
  mappings = MapUserToCoach.objects.filter(Coachid=Coach_id)
  user_ids = mappings.values_list('uuid',flat=True)
  users = User.objects.filter(id__in=user_ids)
  serializer = UserSerializer(users, many=True)
  return Response({"User":serializer.data},status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_User_Coach_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapUserToCoach, id=map_id)
    map_to_delete.delete()
    return Response({"detail": " User To Coach Mapping deleted successfully."}, status=status.HTTP_200_OK)