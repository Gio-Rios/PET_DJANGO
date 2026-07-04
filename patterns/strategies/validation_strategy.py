"""
Padrão GoF: Strategy — Validação
---------------------------------
Define uma família de algoritmos de validação intercambiáveis.
Cada estratégia implementa a mesma interface (ValidationStrategy),
permitindo trocar a regra de validação sem alterar o chamador.

Princípio O (SOLID): aberto para extensão (novas estratégias), fechado para
modificação (o chamador não muda ao adicionar novas regras).

Princípio I (SOLID): interface enxuta com um único método `validate`.
"""
from abc import ABC, abstractmethod


class ValidationStrategy(ABC):
    """Interface base para estratégias de validação (Strategy GoF)."""

    @abstractmethod
    def validate(self, data: dict) -> tuple[bool, str]:
        """Valida os dados recebidos.

        Returns:
            (True, '') se válido.
            (False, 'mensagem de erro') se inválido.
        """


class PetCreationValidationStrategy(ValidationStrategy):
    """Estratégia de validação para criação de pet."""

    _REQUIRED = {
        'name': 'O nome é obrigatório!',
        'species': 'A espécie é obrigatória!',
        'size': 'O porte é obrigatório!',
        'sex': 'O sexo é obrigatório!',
        'age': 'A idade é obrigatória!',
        'weight': 'O peso é obrigatório!',
        'color': 'A cor é obrigatória!',
    }

    def validate(self, data: dict) -> tuple[bool, str]:
        for field, message in self._REQUIRED.items():
            if not data.get(field, '').strip():
                return False, message
        return True, ''


class UserRegistrationValidationStrategy(ValidationStrategy):
    """Estratégia de validação para registro de usuário."""

    _REQUIRED = {
        'name': 'O nome é obrigatório!',
        'email': 'O e-mail é obrigatório!',
        'phone': 'O telefone é obrigatório!',
        'password': 'A senha é obrigatória!',
        'confirmpassword': 'A confirmação de senha é obrigatória!',
    }

    def validate(self, data: dict) -> tuple[bool, str]:
        for field, message in self._REQUIRED.items():
            if not data.get(field, '').strip():
                return False, message
        if data.get('password') != data.get('confirmpassword'):
            return False, 'As senhas não conferem!'
        return True, ''


class UserEditValidationStrategy(ValidationStrategy):
    """Estratégia de validação para edição de perfil."""

    _REQUIRED = {
        'name': 'O nome é obrigatório!',
        'email': 'O e-mail é obrigatório!',
        'phone': 'O telefone é obrigatório!',
    }

    def validate(self, data: dict) -> tuple[bool, str]:
        for field, message in self._REQUIRED.items():
            if not data.get(field, '').strip():
                return False, message
        password = data.get('password', '')
        confirmpassword = data.get('confirmpassword', '')
        if password and password != confirmpassword:
            return False, 'As senhas não conferem!'
        return True, ''
