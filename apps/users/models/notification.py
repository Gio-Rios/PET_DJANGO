"""
--- CAMADA: Models (Entidades ORM) ---

Notification registra eventos do fluxo de adoção que o usuário precisa ver
(visita agendada, adoção aceita ou negada).

Princípio S (SOLID): esta classe modela exclusivamente a entidade Notificação.
"""
from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Notificação de um evento do fluxo de adoção para um usuário."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Usuário',
    )
    message = models.CharField('Mensagem', max_length=255)

    # Referência opcional ao pet relacionado ao evento (string para evitar
    # import circular entre os apps users e pets)
    pet = models.ForeignKey(
        'pets.Pet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Pet relacionado',
    )
    is_read = models.BooleanField('Lida', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.user.name}: {self.message}'
