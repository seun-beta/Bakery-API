import django.contrib.auth.password_validation as validators
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core import exceptions
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.encoding import (
    DjangoUnicodeDecodeError,
    force_str,
    smart_bytes,
    smart_str,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from knox.models import AuthToken
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User
from apps.users.tasks import (
    send_account_activation_email,
    send_new_account_activation_email,
    send_password_reset_email,
)


class RegisterUserSerializer(serializers.ModelSerializer):

    """Serializer for user registration by email
    and initial email verification link generation"""

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "password",
            "password2",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"error": "Password fields didn't match."}
            )
        try:
            validators.validate_password(password=attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(str(e))
        return attrs

    @atomic
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)

        request = self.context.get("request")
        current_site = get_current_site(request).domain
        link = reverse("verify_email")
        token = PasswordResetTokenGenerator().make_token(user)
        base_64_email = urlsafe_base64_encode(smart_bytes(user.email))
        absolute_url = (
            settings.APP_SCHEME
            + current_site
            + link
            + "?token="
            + str(token)
            + "&uid="
            + str(base_64_email)
        )

        send_account_activation_email.delay(email=user.email, absolute_url=absolute_url)

        return user


class RequestNewRegistrationLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, max_length=100)

    def validate(self, attrs):
        email = attrs.get("email", "")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        if user.is_verified:
            raise serializers.ValidationError("email is already verified")

        request = self.context.get("request")
        current_site = get_current_site(request).domain
        link = reverse("verify_email")
        base_64_email = urlsafe_base64_encode(smart_bytes(user.email))
        token = PasswordResetTokenGenerator().make_token(user)
        absolute_url = (
            settings.APP_SCHEME
            + current_site
            + link
            + "?token="
            + str(token)
            + "&uid="
            + str(base_64_email)
        )

        send_new_account_activation_email.delay(
            email=user.email, absolute_url=absolute_url
        )

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    def validate(self, attrs):
        token = self.context.get("request").query_params["token"]
        base_64_email = self.context.get("request").query_params["uid"]
        email = smart_str(urlsafe_base64_decode(base_64_email))
        user = User.objects.get(email=email)
        if PasswordResetTokenGenerator().check_token(user, token):
            if not user.is_verified:
                user.is_verified = True
                user.save()

        else:
            raise serializers.ValidationError("Invalid token, try again")
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        token = AuthToken.objects.create(user=user)
        attrs = attrs.update({"token": token})

        return {
            "email": user.email,
            "token": token[1],
        }


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    def validate(self, attrs):

        email = attrs.get("email")
        request = self.context.get("request")
        redirect_url = attrs.get("redirect_url", "")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            base_64_email = urlsafe_base64_encode(smart_bytes(user.email))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            link = reverse(
                "password-reset-confirm",
                kwargs={"base_64_email": base_64_email, "token": token},
            )
            absolute_url = settings.APP_SCHEME + current_site + link

            url = absolute_url + "?redirect_url=" + redirect_url

            send_password_reset_email.delay(email=user.email, absolute_url=url)
        else:
            pass
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    new_password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]

    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        old_password = attrs.get("old_password", "")
        try:
            user = auth.authenticate(email=user.email, password=old_password)
        except Exception:
            raise serializers.ValidationError({"error": "Wrong password"})
        try:
            validators.validate_password(password=attrs["new_password"])
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        request.user.auth_token_set.all().delete()

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        new_password = validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        token = AuthToken.objects.create(user=user)

        return token[1]


class PasswordTokenCheckSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            base_64_email = self.context.get("request").path.split("/")[3]
            token = self.context.get("request").path.split("/")[4]
            redirect_url = self.context.get("request").query_params["redirect_url"]
            email = smart_str(urlsafe_base64_decode(base_64_email))
            user = User.objects.get(email=email)

            if not PasswordResetTokenGenerator().check_token(user, token):

                if len(redirect_url) > 3:
                    final_url = redirect_url + "?token_valid=False"
                    return final_url
                else:
                    final_url = settings.FRONTEND_URL + "?token_valid=False"
                    return final_url
            if redirect_url and len(redirect_url) > 3:
                final_url = (
                    redirect_url
                    + "?token_valid=True&message=Credentials Valid&base_64_email="
                    + base_64_email
                    + "&token="
                    + token
                )
                return final_url
            else:
                final_url = settings.FRONTEND_URL + "?token_valid=False"
                return final_url

        except DjangoUnicodeDecodeError:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    final_url = redirect_url + "?token_valid=False"
                    return final_url
            except UnboundLocalError:
                raise serializers.ValidationError(
                    "Token is not valid, please request a new one"
                )


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    base_64_email = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ["password", "token", "base_64_email"]

    def validate(self, attrs):
        try:
            breakpoint()

            token = attrs.get("token")
            base_64_email = attrs.get("base_64_email")
            password = attrs.get("password")

            email = force_str(urlsafe_base64_decode(base_64_email))
            user = User.objects.get(email=email)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)
            attrs.pop("token")
            attrs.pop("base_64_email")
            user.set_password(password)
            user.save

            return attrs

        except Exception:
            raise AuthenticationFailed("The reset link is invalid", 401)

    def update(self, instance, validated_data):

        user = validated_data["user"]
        password = validated_data["password"]
        user.set_password(password)
        user.save()

        return user
