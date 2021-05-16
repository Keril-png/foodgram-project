from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class LoginView(FormView):
    template_name = "login.html"


class LogoutView(TemplateView):
    template_name = "logged_out.html"


class PasswordChangeView(FormView):
    template_name = "password_change_form.html"


class PasswordChangeDoneView(TemplateView):
    template_name = "password_change_done.html"


@login_required
def profile(request):
    return redirect(reverse('index'))
