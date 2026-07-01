"""
--- CAMADA: Services (Regras de Negócio) ---

Toda a lógica de negócio relacionada a usuários vive aqui.
Views nunca tomam decisões de negócio — apenas chamam o serviço e retornam.

Princípio S (SOLID): serviço responsável exclusivamente pelas regras do domínio.
Princípio D (SOLID): dependências (factory, repository, strategy) injetadas.
"""
from apps.users.factories import UserFactory
from apps.users.models import CustomUser
from apps.users.repositories import UserRepository
from patterns.singleton import app_config
from patterns.strategies.validation_strategy import (
    UserEditValidationStrategy,
    UserRegistrationValidationStrategy,
)


class UserService:
    """Serviço de regras de negócio para usuários."""

    def __init__(
        self,
        repository: UserRepository | None = None,
        factory: type[UserFactory] | None = None,
    ):
        # Princípio D: dependências injetáveis; defaults convenientes
        self.repo = repository or UserRepository()
        self.factory = factory or UserFactory

    def register(self, data: dict) -> CustomUser:
        """Registra um novo usuário aplicando todas as regras de negócio."""
        # Strategy Pattern: delega validação à estratégia correta
        validator = UserRegistrationValidationStrategy()
        valid, message = validator.validate(data)
        if not valid:
            raise ValueError(message)

        if self.repo.email_in_use(data['email']):
            raise ValueError('Por favor, utilize outro e-mail!')

        user = self.factory.create(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phone=data['phone'],
        )
        app_config.log_info(f'Novo usuário registrado: {user.email}')
        return user

    def edit_profile(self, user: CustomUser, data: dict, image_file=None) -> CustomUser:
        """Edita o perfil do usuário com validação de regras de negócio."""
        validator = UserEditValidationStrategy()
        valid, message = validator.validate(data)
        if not valid:
            raise ValueError(message)

        new_email = data['email']
        if self.repo.email_in_use(new_email, exclude_id=user.pk):
            raise ValueError('Por favor, utilize outro e-mail!')

        user.name = data['name']
        user.email = data['email']
        user.username = data['email']  # mantém username sincronizado
        user.phone = data['phone']

        password = data.get('password', '')
        if password:
            user.set_password(password)

        if image_file:
            # Remove imagem antiga antes de salvar a nova
            if user.image:
                user.image.delete(save=False)
            user.image = image_file

        self.repo.save(user)
        app_config.log_info(f'Perfil atualizado: {user.email}')
        return user
