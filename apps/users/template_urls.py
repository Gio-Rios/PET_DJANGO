"""URLs para views de template (frontend HTML) de usuários."""
from django.urls import path

from apps.users.views.template_views import LoginPageView, ProfilePageView, RegisterPageView

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='page-login'),
    path('register/', RegisterPageView.as_view(), name='page-register'),
    path('profile/', ProfilePageView.as_view(), name='page-profile'),
]
