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
from django.contrib.auth.models import User
from ..serializers import AdminSerializer
from ..models import Admin
from .Maps.MapUserToRole import create_user_role_map, get_role_mapping

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def admin_by_id(request, admin_id):
  admin = get_object_or_404(Admin, id = admin_id)
  serializer = AdminSerializer(instance=admin)
  return Response({"Admin": serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def admins_get_all(request):
  admins = Admin.objects.all()
  serializer = AdminSerializer(admins, many=True)
  return Response({"Admins":serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_admin(request):
    try:
        with transaction.atomic():
            admin_response = make_admin(request.data)
            # user = User.objects.get(username=request.data["username"])
            # if user:
            #     role_mapping_response = get_role_mapping(user.id)
                
            #     if role_mapping_response.get("id"):
            #         if role_mapping_response.get("role") == 1:
            #             admin_response = get_admin(userMapping.get("relatedid"))
            #         else:
            #             raise ValidationError({"detail": "This user is already mapped to a role."})
            #     else:
            #         admin_response = create_admin(request.data)
            #         role_mapping_response = create_user_role_map({
            #             "uuid": user.id,
            #             "role": 1,
            #             "relatedid": admin_response.get("id")
            #         })

            responses = [
                create_user_role_map({
                    "uuid": admin_response.get("id"),
                    "role": 1,
                    "relatedid": admin_response.get("id")
                })
            ]
            
            for response in responses:
                if isinstance(response, Response):
                    return response

    except ValidationError as e:  # Catching ValidationErrors specifically
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
    # serializer = AdminSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response({"Admin": serializer.data},status=status.HTTP_200_OK)
    # return Response(
    #     serializer.errors, status=status.HTTP_400_BAD_REQUEST
    # )

def make_admin(data):
    serializer = AdminSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return Response(serializer.errors)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_admin(request):
    admin = get_object_or_404(Admin, id=request.data["id"])
    admin.first_name = request.data["first_name"]
    admin.last_name = request.data["last_name"]
    admin.save()

    serializer = AdminSerializer(instance=admin)
    return Response({"Admin": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_admin(request, admin_id):
    admin = get_object_or_404(Admin, id=admin_id)
    admin.delete()
    return Response({"Detail": "Admin deleted successfully."}, status=status.HTTP_200_OK)