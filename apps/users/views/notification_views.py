"""
--- CAMADA: Views / Controllers (DRF) ---

Views para o sino de notificações: listagem e marcação de leitura.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import NotificationSerializer
from apps.users.services import NotificationService


class NotificationListView(APIView):
    """GET /api/users/notifications/ — Lista notificações do usuário e a contagem de não lidas."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = NotificationService()
        notifications = service.list_for_user(request.user)
        return Response({
            'notifications': NotificationSerializer(notifications, many=True).data,
            'unread_count': service.unread_count(request.user),
        })


class NotificationMarkReadView(APIView):
    """PATCH /api/users/notifications/<id>/read/ — Marca uma notificação como lida."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        NotificationService().mark_read(pk, request.user)
        return Response({'message': 'Notificação marcada como lida.'})


class NotificationMarkAllReadView(APIView):
    """PATCH /api/users/notifications/read-all/ — Marca todas as notificações como lidas."""

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        NotificationService().mark_all_read(request.user)
        return Response({'message': 'Notificações marcadas como lidas.'})
