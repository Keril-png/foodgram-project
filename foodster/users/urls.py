
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("accounts/profile/", views.profile, name="profile"),
    path("", include("django.contrib.auth.urls")),
]
