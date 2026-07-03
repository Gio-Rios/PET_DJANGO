"""
--- CAMADA: Repositories (Acesso a Dados) ---

Encapsula as queries do ORM referentes a Notification.

Princípio D (SOLID): services dependem desta interface de repositório.
"""
from apps.users.models import Notification


class NotificationRepository:
    """Repositório de acesso a dados para Notification."""

    @staticmethod
    def create(user, message: str, pet=None) -> Notification:
        return Notification.objects.create(user=user, message=message, pet=pet)

    @staticmethod
    def get_by_user(user, limit: int = 30):
        return (
            Notification.objects
            .filter(user=user)
            .select_related('pet')
            [:limit]
        )

    @staticmethod
    def get_unread_count(user) -> int:
        return Notification.objects.filter(user=user, is_read=False).count()

    @staticmethod
    def mark_read(notification_id: int, user) -> None:
        Notification.objects.filter(pk=notification_id, user=user).update(is_read=True)

    @staticmethod
    def mark_all_read(user) -> None:
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)
