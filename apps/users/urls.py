from django.urls import path

from apps.users.views import (
    ChangePasswordView,
    LoginView,
    PasswordTokenCheckView,
    RegisterView,
    RequestNewRegistrationLinkView,
    RequestPasswordResetView,
    SetNewPasswordAPIView,
    VerifyEmailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "new-registration-link/",
        RequestNewRegistrationLinkView.as_view(),
        name="new_registration_link",
    ),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "request-password-reset/",
        RequestPasswordResetView.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<base_64_email>/<token>/",
        PasswordTokenCheckView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path("change-password", ChangePasswordView.as_view(), name="change_password"),
]
