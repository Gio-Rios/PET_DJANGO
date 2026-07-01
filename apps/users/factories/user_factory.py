"""
Padrão GoF: Factory — UserFactory
-----------------------------------
Centraliza a criação de instâncias de CustomUser, encapsulando a lógica
de hash de senha (set_password) e a derivação do username.

Princípio S (SOLID): a factory é responsável apenas pela criação do objeto;
a lógica de negócio de registro fica no UserService.
"""
from apps.users.models import CustomUser


class UserFactory:
    """Fábrica para criação de instâncias de CustomUser (Factory GoF)."""

    @staticmethod
    def create(*, name: str, email: str, password: str, phone: str) -> CustomUser:
        """Cria e persiste um novo usuário com senha hasheada via PBKDF2."""
        user = CustomUser(name=name, email=email, phone=phone)
        user.set_password(password)  # Django gera hash PBKDF2 automaticamente
        user.save()
        return user

    @staticmethod
    def build(*, name: str, email: str, password: str, phone: str) -> CustomUser:
        """Constrói um CustomUser em memória sem persistir (útil em testes)."""
        user = CustomUser(name=name, email=email, phone=phone)
        user.set_password(password)
        return user
