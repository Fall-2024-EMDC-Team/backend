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

from ..models import Organizer
from ..serializers import OrganizerSerializer

@api_view(["GET"])
def organizer_by_id(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    serializer = OrganizerSerializer(instance=organizer)
    return Response({"organizer": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_organizer(request):
    serializer = OrganizerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"organizer": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_organizer(request):
    organizer = get_object_or_404(Organizer, id=request.data["id"])
    organizer.first_name = request.data["first_name"]
    organizer.last_name = request.data["last_name"]
    organizer.region = request.data["region"]
    organizer.save()

    serializer = OrganizerSerializer(instance=organizer)
    return Response({"organizer": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_organizer(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    organizer.delete()
    return Response({"detail": "Organizer deleted successfully."}, status=status.HTTP_200_OK)

@api_view(["GET"])
def organizers(request):
    organizers = Organizer.objects.all()
    serializer = OrganizerSerializer(organizers, many=True)
    return Response({"organizer": serializer.data}, status=status.HTTP_200_OK)