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
from ..models import Coach
from ..serializers import CoachSerializer

@api_view(["GET"])
def coach_by_id(request, coach_id):
  contest = get_object_or_404(Coach, id = coach_id)
  serializer = CoachSerializer(instance=contest)
  return Response({"Coach": serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
def coach_get_all(request):
  coaches = Coach.objects.all()
  serializer = CoachSerializer(coaches, many=True)
  return Response({"Coaches":serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_coach(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"coach": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_coach(request):
    coach = get_object_or_404(Coach, id=request.data["id"])
    coach.first_name = request.data["first_name"]
    coach.last_name = request.data["last_name"]
    coach.school_name = request.data["school_name"]
    coach.save()

    serializer = CoachSerializer(instance=coach)
    return Response({"coach": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_coach(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    coach.delete()
    return Response({"detail": "Coach deleted successfully."}, status=status.HTTP_200_OK)