from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from ..views.Maps.MapUserToRole import get_role

@api_view(["GET"])
def user_by_id(request, user_id):  # Consistent parameter name
    user = get_object_or_404(User, id=user_id)  # Use user_id here
    serializer = UserSerializer(instance=user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


# login endpoint
@api_view(["POST"])
def login(request):
    user = get_object_or_404(
        User, username=request.data["username"]
    )  # check if user's email exists
    if not user.check_password(request.data["password"]):  # if password is incorrect
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    userSerializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": userSerializer.data, "role":get_role(user.id)})


# signup endpoint
@api_view(["POST"])
def signup(request):
    try:
        user_data = request.data
        result = create_user(user_data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# delete user by id
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_by_id(request, user_id):
    delete_user(user_id)
    return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)


# edit user (password change, email change) API
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request):
    user = get_object_or_404(User, id=request.data["id"])

    try:
        if request.data["username"] != user.username:
            if User.objects.filter(username=request.data["username"]).exists():
                return Response(
                    {"detail": "Email already taken."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.username = request.data["username"]
    except:
        pass

    try:
        if request.data["password"] != user.password:
            user.set_password(request.data["password"])
    except:
        pass

    user.save()
    serializer = UserSerializer(instance=user)

    return Response({"user": serializer.data})


# token verification endpoint
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"passed for {}".format(request.user.username)})


def create_user(user_data):
    if User.objects.filter(username=user_data["username"]).exists():
        raise ValidationError("Username already exists.")

    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            user.set_password(user_data["password"])
            user.save()
            token = Token.objects.create(user=user)
            return {"token": token.key, "user": serializer.data}

    raise ValidationError(serializer.errors)

def delete_user(uuid):
    user_to_delete = get_object_or_404(User, id=uuid)
    user_to_delete.delete()

