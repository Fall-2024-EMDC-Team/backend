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

from ...models import MapUserToOrganizer, Organizer, User
from ...serializers import MapUserToOrganizerSerializer, OrganizerSerializer, UserSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_organizer_mapping(request):
  serializer = MapUserToOrganizerSerializer(data=request.data)
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
def get_organizer_by_user_id(request, uuid_id):
  organizer_ids = MapUserToOrganizer.objects.filter(request.data["id"])
  organizers = Organizer.objects.filter(id__in=organizer_ids)
  serializer = OrganizerSerializer(organizers, many=True)
  return Response({"Organizers":serializer.data()},status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_organizer_id(request,organizer_id):
  mappings = MapUserToOrganizer.objects.filter(organizerid=organizer_id)
  user_ids = mappings.values_list('uuid',flat=True)
  users = User.objects.filter(id__in=user_ids)
  serializer = UserSerializer(users, many=True)
  return Response({"User":serializer.data},status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_User_organizer_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapUserToOrganizer, id=map_id)
    map_to_delete.delete()
    return Response({"detail": " User To Organizer Mapping deleted successfully."}, status=status.HTTP_200_OK)