"""
--- CAMADA: Serializers (Validação e Serialização) ---

Responsáveis por converter dados de entrada (JSON/form) em objetos Python
e vice-versa. Não contêm regras de negócio — apenas estrutura dos dados.

Princípio S (SOLID): cada serializer tem uma responsabilidade bem definida.
"""
from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializa CustomUser para leitura (sem expor a senha)."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'image']
        read_only_fields = ['id']

    def get_image(self, obj) -> str | None:
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class RegisterSerializer(serializers.Serializer):
    """Deserializa e valida dados de registro. Não persiste — delega ao service."""

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, min_length=6)
    confirmpassword = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    """Deserializa credenciais de login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserEditSerializer(serializers.Serializer):
    """Deserializa dados de edição de perfil."""

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    confirmpassword = serializers.CharField(write_only=True, required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)
