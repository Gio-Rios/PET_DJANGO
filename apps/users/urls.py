"""URLs da API REST para usuários."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views.notification_views import (
    NotificationListView,
    NotificationMarkAllReadView,
    NotificationMarkReadView,
)
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
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/read-all/', NotificationMarkAllReadView.as_view(), name='notification-read-all'),
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-read'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/edit/', UserEditView.as_view(), name='user-edit'),
]
