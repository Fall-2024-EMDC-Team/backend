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
from ..serializers import AdminSerializer
from ..models import Admin

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
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Admin": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

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