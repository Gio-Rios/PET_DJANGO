"""Views que renderizam templates HTML (frontend via Django templates + JS fetch)."""
from django.views.generic import TemplateView


class LoginPageView(TemplateView):
    template_name = 'users/login.html'


class RegisterPageView(TemplateView):
    template_name = 'users/register.html'


class ProfilePageView(TemplateView):
    template_name = 'users/profile.html'
