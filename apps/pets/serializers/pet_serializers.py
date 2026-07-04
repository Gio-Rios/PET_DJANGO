"""
--- CAMADA: Serializers (Validação e Serialização) ---

Convertem instâncias de Pet para JSON e validam dados de entrada.
Não contêm regras de negócio — apenas estrutura e formato dos dados.

Princípio S (SOLID): cada serializer tem uma única responsabilidade.
"""
from rest_framework import serializers

from apps.pets.models import Pet, PetImage


class PetImageSerializer(serializers.ModelSerializer):
    """Serializa imagens de pet com URL absoluta."""

    class Meta:
        model = PetImage
        fields = ['id', 'image', 'is_cover']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.image:
            rep['image'] = request.build_absolute_uri(instance.image.url)
        return rep


class PetSerializer(serializers.ModelSerializer):
    """Serializa Pet completo para leitura (com imagens e dados do dono)."""

    images = PetImageSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    owner_phone = serializers.CharField(source='owner.phone', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    adopter_name = serializers.SerializerMethodField()
    adopter_image = serializers.SerializerMethodField()
    species_label = serializers.CharField(source='get_species_label', read_only=True)
    size_label = serializers.CharField(source='get_size_display', read_only=True)
    sex_label = serializers.CharField(source='get_sex_display', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'species', 'species_other', 'species_label', 'size', 'size_label',
            'sex', 'sex_label',
            'age', 'weight', 'color', 'available',
            'owner', 'owner_name', 'owner_phone', 'owner_email',
            'adopter', 'adopter_name', 'adopter_image',
            'images', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'owner', 'adopter', 'available', 'created_at', 'updated_at',
        ]

    def get_adopter_name(self, obj) -> str | None:
        return obj.adopter.name if obj.adopter else None

    def get_adopter_image(self, obj) -> str | None:
        request = self.context.get('request')
        if obj.adopter and obj.adopter.image and request:
            return request.build_absolute_uri(obj.adopter.image.url)
        return None


class PetCreateSerializer(serializers.Serializer):
    """Deserializa dados para criação/atualização de pet (sem ORM direto)."""

    name = serializers.CharField(max_length=100)
    species = serializers.ChoiceField(choices=Pet.SPECIES_CHOICES)
    species_other = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')
    size = serializers.ChoiceField(choices=Pet.SIZE_CHOICES)
    sex = serializers.ChoiceField(choices=Pet.SEX_CHOICES)
    age = serializers.CharField(max_length=50)
    weight = serializers.CharField(max_length=50)
    color = serializers.CharField(max_length=50)
    cover_index = serializers.IntegerField(required=False, default=0, min_value=0)
    cover_existing_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    delete_image_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list,
    )
