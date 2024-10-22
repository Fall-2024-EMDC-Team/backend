from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ...auth.serializers import UserSerializer
from ...models import MapUserToRole, Coach, Organizer, Judge, Admin
from ...serializers import MapUserToRoleSerializer, CoachSerializer, OrganizerSerializer, JudgeSerializer, AdminSerializer
from django.shortcuts import get_object_or_404

#from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_role_mapping(request):
    try:
        # Call the function that creates the user-role mapping
        mapping = create_user_role_map(request.data)  # This function can raise ValidationError
        return Response(mapping, status=status.HTTP_201_CREATED)  # If successful, return the mapping

    except ValidationError as e:
        # Handle validation errors and return a 400 response
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle any other exceptions
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def login_return(request, userid):
    return Response(get_role(userid), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_role(request, relatedid, roleType):
    mapping = MapUserToRole.objects.get(relatedid=relatedid, role=roleType)
    uuid = mapping.uuid
    user = get_object_or_404(User, id=uuid)
    serializer = UserSerializer(instance=user)
    return Response({"User": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_by_user(request, userid):
    mapping = MapUserToRole.objects.get(uuid=userid)
    if mapping.role != 1:
        return Response("Error: Given User is Not an Admin", status=status.HTTP_404_NOT_FOUND)
    else:
        adminid = mapping.relatedid
        admin = Admin.objects.get(id=adminid)
        serializer = AdminSerializer(instance=admin)
        return Response({"Admin": serializer.data}, status=status.HTTP_200_OK)

@api_view(["delete"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_role_mapping(request, mapping_id):
    mapping = get_object_or_404(MapUserToRole, id=mapping_id)
    mapping.delete()
    return Response({"detail": "Mapping deleted successfully."}, status=status.HTTP_200_OK)

def get_role(user_id):
    mapping = MapUserToRole.objects.get(uuid=user_id)

    if mapping.role == 1:
        admin = Admin.objects.get(id=mapping.relatedid)
        roleSerializer = AdminSerializer(instance=admin)
        return {"user_type": mapping.role, "user": roleSerializer.data}

    elif mapping.role == 2:
        organizer = Organizer.objects.get(id=mapping.relatedid)
        roleSerializer = OrganizerSerializer(instance=organizer)
        return {"user_type": mapping.role, "user": roleSerializer.data}

    elif mapping.role == 3:
        judge = Judge.objects.get(id=mapping.relatedid)
        roleSerializer = JudgeSerializer(instance=judge)
        return {"user_type": mapping.role, "user": roleSerializer.data}

    elif mapping.role == 4:
        coach = Coach.objects.get(id=mapping.relatedid)
        roleSerializer = CoachSerializer(instance=coach)
        return {"user_type": mapping.role, "user": roleSerializer.data}

def create_user_role_map(mapData):
    existing_mapping = MapUserToRole.objects.filter(uuid=mapData.get("uuid")).first()
    if existing_mapping:
        raise ValidationError({"detail": "This user is already mapped to a role."})

    serializer = MapUserToRoleSerializer(data=mapData)
    if serializer.is_valid():
        serializer.save()
        return serializer.data

    raise ValidationError(serializer.errors)

def get_role_mapping(uuid):
    existing_mapping = MapUserToRole.objects.filter(uuid=uuid).first()
    serializer = MapUserToRoleSerializer(instance=existing_mapping)
    return serializer.data

    raise ValidationError(serializer.errors)
