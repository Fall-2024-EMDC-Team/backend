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
from django.contrib.auth.models import User
from ...models import MapUserToRole, Coach, Organizer, Judge, Admin
from ...serializers import MapUserToRoleSerializer, CoachSerializer, OrganizerSerializer, JudgeSerializer, AdminSerializer

# TO-DO: Add Admin to This

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_role_mapping(request):
  # role should map directly to the ENUM Found in Role Enum, Line 49 in Models.py
  serializer = MapUserToRoleSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response({"mapping": serializer.data},status=status.HTTP_200_OK)
  return Response(
      serializer.errors, status=status.HTTP_400_BAD_REQUEST
  )
  
@api_view(['GET'])
def login_return(request,userid):
  mapping = MapUserToRole.objects.get(uuid=userid)
  if mapping.role == 1:
    admin = Admin.objects.get(id=mapping.relatedid)
    serializer = AdminSerializer(instance=admin)
    return Response({"User Type":mapping.role,"Admin":serializer.data},status=status.HTTP_200_OK)
    
  elif mapping.role == 2:
    organizer = Organizer.objects.get(id=mapping.relatedid)
    serializer = OrganizerSerializer(instance=organizer)
    return Response({"User Type":mapping.role, "User":serializer.data},status=status.HTTP_200_OK)

  elif mapping.role == 3:
    judge = Judge.objects.get(id=mapping.relatedid)
    serializer = JudgeSerializer(instance=judge)
    return Response({"User Type":mapping.role,"User":serializer.data},status=status.HTTP_200_OK)

  elif mapping.role == 4:
    coach = Coach.objects.get(id=mapping.relatedid)
    serializer = CoachSerializer(instance=coach)
    return Response({"User Type":mapping.role,"User":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_coach_by_user(request,userid):
    mapping = MapUserToRole.objects.get(uuid=userid)
    if mapping.role != 4:
      return Request("Error: Given User is Not a Coach",status=status.HTTP_404_NOT_FOUND)
    else:
      coachid = mapping.relatedid
      coach = Coach.objects.get(id=coachid)
      serializer = CoachSerializer(instance=coach)
      return Response({"Coach": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_organizer_by_user(request,userid):
    mapping = MapUserToRole.objects.get(uuid=userid)
    if mapping.role != 2:
        return Request("Error: Given User is Not a Coach",status=status.HTTP_404_NOT_FOUND)
    else:
      organizerid = mapping.relatedid
      organizer = Organizer.objects.get(id=organizerid)
      serializer = OrganizerSerializer(instance=organizer)
      return Response({"Organizer": serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_judge_by_user(request,userid):
    mapping = MapUserToRole.objects.get(uuid=userid)
    if mapping.role != 3:
        return Request("Error: Given User is Not a Judge",status=status.HTTP_404_NOT_FOUND)
    else:
      judgeid = mapping.relatedid
      judge = Judge.objects.get(id=organizerid)
      serializer = JudgeSerializer(instance=organizer)
      return Response({"Judge": serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_by_user(request,userid):
    mapping = MapUserToRole.objects.get(uuid=userid)
    if mapping.role != 1:
        return Request("Error: Given User is Not an Admin",status=status.HTTP_404_NOT_FOUND)
    else:
      adminid = mapping.relatedid
      admin = Admin.objects.get(id=organizerid)
      serializer = AdminSerializer(instance=organizer)
      return Response({"Admin": serializer.data},status=status.HTTP_200_OK)




