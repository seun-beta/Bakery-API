from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    PasswordTokenCheckSerializer,
    RegisterUserSerializer,
    RequestNewRegistrationLinkSerializer,
    RequestPasswordResetSerializer,
    SetNewPasswordSerializer,
    VerifyEmailSerializer,
)


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [settings.PROTOCOL_SCHEME, "http", "https"]


class RegisterView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestNewRegistrationLinkView(GenericAPIView):
    serializer_class = RequestNewRegistrationLinkSerializer
    permission_classes = []

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "Registration link sent to email address successfully"},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    http_method_names = ["get"]
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )
    email_param_config = openapi.Parameter(
        "email",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config, email_param_config])
    def get(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response("email successfully verified", status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestPasswordResetView(GenericAPIView):
    serializer_class = RequestPasswordResetSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = request.user

        return Response(
            {"data": user.tokens()},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckView(GenericAPIView):
    serializer_class = PasswordTokenCheckSerializer
    permission_classes = []

    def get(self, request, base_64_email, token):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return CustomRedirect(serializer.validated_data)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response({"Password changed successfully"}, status=status.HTTP_200_OK)
