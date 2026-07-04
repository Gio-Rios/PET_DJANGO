"""
--- CAMADA: Services (Regras de Negócio) ---

Centraliza a criação e consulta de notificações. Chamado pelo PetService
quando eventos do fluxo de adoção acontecem (agendamento, aceite, negativa).

Princípio D (SOLID): dependências injetáveis (repository).
"""
from apps.users.models import Notification
from apps.users.repositories import NotificationRepository


class NotificationService:
    """Serviço de regras de negócio para notificações do usuário."""

    def __init__(self, repository: NotificationRepository | None = None):
        self.repo = repository or NotificationRepository()

    def notify(self, user, message: str, pet=None) -> Notification:
        return self.repo.create(user, message, pet)

    def list_for_user(self, user):
        return self.repo.get_by_user(user)

    def unread_count(self, user) -> int:
        return self.repo.get_unread_count(user)

    def mark_read(self, notification_id: int, user) -> None:
        self.repo.mark_read(notification_id, user)

    def mark_all_read(self, user) -> None:
        self.repo.mark_all_read(user)
