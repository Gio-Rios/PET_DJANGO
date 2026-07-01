"""
--- CAMADA: Repositories (Acesso a Dados) ---

Encapsula as queries do ORM do Django para CustomUser.
As camadas superiores (services, views) nunca chamam o ORM diretamente —
sempre passam pelo repositório.

Princípio D (SOLID): services dependem desta abstração de repositório,
não da implementação concreta do ORM.
"""
from apps.users.models import CustomUser


class UserRepository:
    """Repositório de acesso a dados para CustomUser."""

    @staticmethod
    def get_by_email(email: str) -> CustomUser | None:
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def get_by_id(user_id: int) -> CustomUser | None:
        return CustomUser.objects.filter(pk=user_id).first()

    @staticmethod
    def email_in_use(email: str, exclude_id: int | None = None) -> bool:
        qs = CustomUser.objects.filter(email=email)
        if exclude_id is not None:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()

    @staticmethod
    def save(user: CustomUser) -> CustomUser:
        user.save()
        return user
