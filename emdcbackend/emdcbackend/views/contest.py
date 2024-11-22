from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..models import Contest
from ..serializers import ContestSerializer
from .clusters import create_cluster, make_cluster
from .Maps.MapClusterToContest import map_cluster_to_contest,create_cluster_contest_mapping

# TO-DO: Add Get Contest by Date/Time

# get a contest by a certain id:
@api_view(["GET"])
def contest_by_id(request, contest_id):
  contest = get_object_or_404(Contest, id = contest_id)
  serializer = ContestSerializer(instance=contest)
  return Response({"Contest": serializer.data}, status=status.HTTP_200_OK)

# get all contests
@api_view(["GET"])
def contest_get_all(request):
  contests = Contest.objects.all()
  serializer = ContestSerializer(instance=contests, many=True)
  return Response({"Contests":serializer.data}, status=status.HTTP_200_OK)

# Create contest and Map to empty cluster
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest(request):
  try:
      with transaction.atomic():
        all_teams = make_cluster({"cluster_name": "All Teams"})
        contest = create_contest_instance({"name": request.data["name"], "date": request.data["date"], "is_open":False,"is_tabulated":False})
        responses = [
          map_cluster_to_contest({
              "contestid": contest.get("id"),
              "clusterid": all_teams.get("id")
          }), 
        ]
        for response in responses:
          if isinstance(response, Response):
              return response

        return Response({
          "contest": contest,
          "contest_map": responses[0],
      }, status=status.HTTP_201_CREATED)

  except ValidationError as e:  # Catching ValidationErrors specifically
      return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
      return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
# Helper method to create contest
def create_contest_instance(contest_data):
  serializer = ContestSerializer(data=contest_data)
  if serializer.is_valid():
      serializer.save()
      return serializer.data
  raise ValidationError(serializer.errors)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_contest(request):
  contest = get_object_or_404(Contest, id=request.data["id"])
  contest.name = request.data["name"]
  contest.date = request.data["date"]
  contest.is_open = request.data["is_open"]
  contest.is_tabulated = request.data["is_tabulated"]
  contest.save()
  serializer = ContestSerializer(instance=contest)
  return Response({"Contest":serializer.data}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest(request,contest_id):
  contest = get_object_or_404(Contest, id=contest_id)
  contest.delete()
  return Response({"detail": "Contest deleted successfully."}, status=status.HTTP_200_OK)

