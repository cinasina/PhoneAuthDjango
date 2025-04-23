from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify/otp/", views.VerifyOTPView.as_view(), name="verify-otp"),
    path("set-password/", views.SetPasswordView.as_view(), name="set-password"),
    path(
        "user-info/", views.CompleteProfileView.as_view(), name="complete-profile"
    ),
    path("login/", views.LoginView.as_view(), name="login"),
]
