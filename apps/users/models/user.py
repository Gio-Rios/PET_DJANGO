"""
--- CAMADA: Models (Entidades ORM) ---

Princípio S (SOLID): esta classe é responsável exclusivamente pela definição
da entidade de domínio User — sem lógica de negócio nem validação de formulário.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Usuário customizado com campos adicionais do domínio Get a Pet.

    Herda de AbstractUser: password (hash PBKDF2), is_active, date_joined, etc.
    Autentica via e-mail em vez de username.
    """

    # Permite username vazio (gerado automaticamente a partir do email)
    username = models.CharField(max_length=150, unique=True, blank=True)

    name = models.CharField('Nome completo', max_length=100)
    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Telefone', max_length=20)
    image = models.ImageField('Foto de perfil', upload_to='users/', null=True, blank=True)

    # Usamos email como campo de identificação principal
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self) -> str:
        return f'{self.name} <{self.email}>'

    def save(self, *args, **kwargs):
        # Garante username único derivado do email quando não informado
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
