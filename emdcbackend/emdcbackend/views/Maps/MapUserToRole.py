from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    user_uuid = request.data.get('uuid')  # Assuming uuid is passed in the request data
    role = request.data.get('role')
    relatedid = request.data.get('relatedid')

    return create_user_role_map(user_uuid, role, relatedid)  # Return the response from this function

@api_view(['GET'])
def login_return(request, userid):
    return Response(get_role(userid), status=status.HTTP_200_OK)

# The other 'get_' functions remain unchanged...

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

def create_user_role_map(uuid, role, roleObjectId):
    # Check if the uuid is already mapped to a role
    existing_mapping = MapUserToRole.objects.filter(uuid=uuid).first()

    if existing_mapping:
        return Response(
            {"detail": "This user is already mapped to a role."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the serializer with the data keyword argument
    serializer = MapUserToRoleSerializer(data={"uuid": uuid, "role": role, "relatedid": roleObjectId})

    if serializer.is_valid():
        serializer.save()
        return Response({"mapping": serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
