from rest_framework import status
from rest_framework.decorators import (
  api_view,
  authentication_classes,
  permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ...models import MapContestToOrganizer, Organizer, Contest
from ...serializers import MapContestToOrganizerSerializer, ContestSerializer, OrganizerSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest_organizer_mapping(request):
    try:
        map_data = request.data
        result = map_contest_to_organizer(map_data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def map_contest_to_organizer(map_data):
    serializer = MapContestToOrganizerSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_organizers_by_contest_id(request, contest_id):
  organizer_ids = MapContestToOrganizer.objects.filter(contestid=contest_id)
  organizers = Organizer.objects.filter(id__in=organizer_ids)
  serializer = OrganizerSerializer(organizers, many=True)
  return Response({"Organizers": serializer.data},status=status.HTTP_200_OK)

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

# endpoint that returns all the contests and their organizers
# key: contestid, value: list of organizer objects

