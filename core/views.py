from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, EmailLog
from .serializers import UserCreateSerializer
from .tasks import send_activation_email
from . import utils


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        # Here, we are sure that user can be created with no error
        instance = serializer.save()

        # So, we send an verification email
        send_activation_email.delay(instance.pk, instance.email)
        email_log = EmailLog(user=instance, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()


class UserActivateView(APIView):
    def get(self, request, uid, token):
        user = utils.get_user_from_token(uid, token)
        if user:
            user.is_email_activated = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'error': 'Token is invalid.'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
