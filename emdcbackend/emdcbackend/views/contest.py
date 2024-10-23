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
from django.db import transaction
from ..models import Contest
from ..serializers import ContestSerializer
from .Maps.MapContestToOrganizer import create_contest_organizer_mapping

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

# create contest
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest(request):
  try:
    with transaction.atomic():
      contest_response = make_contest(request.data)
      response = [
        create_contest_organizer_mapping({
          "contestid": contest_response.get("id"),
          "organizerid": request.data["organizerid"]
        })
      ]
  
  except ValidationError as e:  # Catching ValidationErrors specifically
    return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  
  except Exception as e:
    return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
  # serializer = ContestSerializer(data=request.data)
  # if serializer.is_valid():
  #   serializer.save()
  #   return Response({"Contest": serializer.data},status = status.HTTP_200_OK)
  # return Response(
  #       serializer.errors, status=status.HTTP_400_BAD_REQUEST
  #   )

def make_contest(data):
  serializer = ContestSerializer(data=data)
  if serializer.is_valid():
    serializer.save()
    return serializer.data
  return Response(serializer.errors)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_contest(request):
  contest = get_object_or_404(Contest, id=request.data["id"])
  contest.name = request.data["name"]
  contest.is_open = request.data["is_open"]
  contest.is_tabulated = request.data["is_tabulated"]
  contest.save()
  serializer = ContestSerializer(instance=contest)
  return Response({"Contest":serializer.data}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest(request,contest_id):
  contest = get_object_or_404(Contest, contest_id)
  contest.delete()
  return Response({"detail": "Contest deleted successfully."}, status=status.HTTP_200_OK)