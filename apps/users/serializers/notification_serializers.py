"""
--- CAMADA: Serializers (Validação e Serialização) ---

Serializa notificações para exibição no sino de avisos do frontend.
"""
from rest_framework import serializers

from apps.users.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializa Notification para leitura."""

    pet_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'pet_id', 'is_read', 'created_at']

    def get_pet_id(self, obj) -> int | None:
        return obj.pet_id
