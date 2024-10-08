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

from ...models import MapContestToOrganizer, Organizer, Contest
from ...serializers import MapContestToOrganizerSerializer, ContestSerializer, OrganizerSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest_organizer_mapping(request):
  serializer = MapContestToOrganizerSerializer(data=request.data)
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
def get_organizers_by_contest_id(request, contest_id):
  organizer_ids = MapContestToOrganizer.objects.filter(request.data["id"])
  organizers = Organizer.objects.filter(id__in=organizer_ids)
  serializer = OrganizerSerializer(organizers, many=True)
  return Response({"Judges":serializer.data()},status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_contests_by_organizer_id(request,organizer_id):
  mappings = MapContestToOrganizer.objects.filter(organizerid=organizer_id)
  contest_ids = mappings.values_list('contestid',flat=True)
  contests = Contest.objects.filter(id__in=contest_ids)
  serializer = ContestSerializer(contests, many=True)
  return Response({"Contests":serializer.data},status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest_organizer_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapContestToOrganizer, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Contest To Organizer Mapping deleted successfully."}, status=status.HTTP_200_OK)