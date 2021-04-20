
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("", include("django.contrib.auth.urls")),
    #path("reset/done/", PasswordResetDoneView.as_view(
    #    template_name="registration/password_reset_done.html"),
    #     name="password_reset_done"),
    #path('login/', views.LoginView.as_view(), name='login'),
]
