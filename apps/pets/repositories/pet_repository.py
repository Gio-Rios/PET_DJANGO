"""
--- CAMADA: Repositories (Acesso a Dados) ---

Encapsula todas as queries do ORM referentes a Pet e PetImage.
O service nunca toca o ORM diretamente.

Princípio D (SOLID): services dependem desta interface de repositório.
"""
from apps.pets.models import Pet, PetImage


class PetRepository:
    """Repositório de acesso a dados para Pet e PetImage."""

    @staticmethod
    def get_all():
        """Retorna todos os pets com joins otimizados."""
        return (
            Pet.objects
            .select_related('owner', 'adopter')
            .prefetch_related('images')
            .order_by('-created_at')
        )

    @staticmethod
    def get_by_id(pet_id: int) -> Pet | None:
        return (
            Pet.objects
            .select_related('owner', 'adopter')
            .prefetch_related('images')
            .filter(pk=pet_id)
            .first()
        )

    @staticmethod
    def get_by_owner(user):
        return (
            Pet.objects
            .filter(owner=user)
            .prefetch_related('images')
            .order_by('-created_at')
        )

    @staticmethod
    def get_by_adopter(user):
        return (
            Pet.objects
            .filter(adopter=user)
            .prefetch_related('images')
            .order_by('-created_at')
        )

    @staticmethod
    def save(pet: Pet) -> Pet:
        pet.save()
        return pet

    @staticmethod
    def delete(pet: Pet) -> None:
        pet.delete()

    @staticmethod
    def add_image(pet: Pet, image_file, is_cover: bool = False) -> PetImage:
        return PetImage.objects.create(pet=pet, image=image_file, is_cover=is_cover)

    @staticmethod
    def delete_images(pet: Pet) -> None:
        for img in pet.images.all():
            img.image.delete(save=False)
            img.delete()

    @staticmethod
    def delete_images_by_ids(pet: Pet, image_ids: list) -> None:
        for img in pet.images.filter(pk__in=image_ids):
            img.image.delete(save=False)
            img.delete()

    @staticmethod
    def set_cover(pet: Pet, image_id: int) -> None:
        pet.images.update(is_cover=False)
        pet.images.filter(pk=image_id).update(is_cover=True)
