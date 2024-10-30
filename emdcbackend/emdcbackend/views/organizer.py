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
from django.db import transaction
from ..models import Organizer
from ..serializers import OrganizerSerializer
from ..auth.views import create_user
from .Maps.MapUserToRole import create_user_role_map
from .Maps.MapContestToOrganizer import map_contest_to_organizer

# get organizer by id
@api_view(["GET"])
def organizer_by_id(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    serializer = OrganizerSerializer(instance=organizer)
    return Response({"organizer": serializer.data}, status=status.HTTP_200_OK)

# create an organizer
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_organizer(request):
    try:
        with transaction.atomic():
            user_response, organizer_response = create_user_and_organizer(request.data)  # creates user and organizer
            responses = [
                create_user_role_map({  # maps the newly-created user to the role of an organizer
                    "uuid": user_response.get("user").get("id"),
                    "role": 2,
                    "relatedid": organizer_response.get("id")
                }),
                map_contest_to_organizer({  # maps the newly-created organizer to a contest
                    "contestid": request.data["contestid"],
                    "organizerid": organizer_response.get("id")
                })
            ]
            for response in responses:
                if isinstance(response, Response):
                    return response
                
            return Response({
                "user": user_response,
                "organizer": organizer_response,
                "user_map": responses[0],
                "organizer to contest map": responses[1]
            }, status=status.HTTP_201_CREATED)

    except ValidationError as e:  # Catching ValidationErrors specifically
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_user_and_organizer(data):
    user_data = {"username": data["username"], "password": data["password"]}
    user_response = create_user(user_data)
    if not user_response.get('user'):
        raise ValidationError('User creation failed.')
    
    organizer_data = {"first_name": data["first_name"], "last_name": data["last_name"]}
    organizer_response = make_organizer(organizer_data)
    if not organizer_response.get('id'):
        raise ValidationError('Organizer creation failed.')
    
    return user_response, organizer_response

def make_organizer(organizer_data):
    serializer = OrganizerSerializer(data=organizer_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise ValidationError(serializer.errors)

# edit an organizer
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

# delete an organizer by a certain id
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_organizer(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    organizer.delete()
    return Response({"detail": "Organizer deleted successfully."}, status=status.HTTP_200_OK)

# return all organizers
@api_view(["GET"])
def organizers(request):
    organizers = Organizer.objects.all()
    serializer = OrganizerSerializer(organizers, many=True)
    return Response({"organizer": serializer.data}, status=status.HTTP_200_OK)