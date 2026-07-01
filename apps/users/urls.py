"""URLs da API REST para usuários."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views.user_views import (
    CheckUserView,
    LoginView,
    RegisterView,
    UserDetailView,
    UserEditView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('checkuser/', CheckUserView.as_view(), name='user-check'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/edit/', UserEditView.as_view(), name='user-edit'),
]
