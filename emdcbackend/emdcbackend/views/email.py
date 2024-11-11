from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_email(request):
    try:
        address = request.data["address"]
        subject = request.data["subject"]
        message = request.data["message"]

        send_mail(subject, message, settings.EMAIL_HOST_USER, [address])

    except ValidationError as e:
        # Specific error handling for validation errors
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # General error handling
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)