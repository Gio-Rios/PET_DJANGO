"""
--- CAMADA: Services (Regras de Negócio) ---

Toda a lógica de adoção vive aqui — não nas views, não nos serializers.
Views apenas chamam o serviço e devolvem a resposta HTTP.

Princípio S (SOLID): serviço responsável exclusivamente pelas regras do domínio.
Princípio D (SOLID): dependências injetadas (factory, repository, strategy).
"""
from apps.pets.factories import PetFactory
from apps.pets.models import Pet
from apps.pets.repositories import PetRepository
from apps.users.services import NotificationService
from patterns.singleton import app_config
from patterns.strategies.validation_strategy import PetCreationValidationStrategy


class PetService:
    """Serviço de regras de negócio para Pets e fluxo de adoção."""

    def __init__(
        self,
        repository: PetRepository | None = None,
        factory: type[PetFactory] | None = None,
        notification_service: NotificationService | None = None,
    ):
        # Princípio D: dependências injetáveis; defaults convenientes
        self.repo = repository or PetRepository()
        self.factory = factory or PetFactory
        self.notifications = notification_service or NotificationService()

    def create_pet(self, owner, data: dict, image_files: list) -> Pet:
        """Cria um pet com imagens, aplicando validação por Strategy."""
        # Strategy Pattern: delega a validação à estratégia correta
        validator = PetCreationValidationStrategy()
        valid, message = validator.validate(data)
        if not valid:
            raise ValueError(message)

        if not image_files:
            raise ValueError('A imagem é obrigatória!')
        if len(image_files) > 4:
            raise ValueError('Você pode enviar no máximo 4 fotos por pet.')

        # Factory Pattern: cria a entidade Pet
        pet = self.factory.create(
            owner=owner,
            name=data['name'],
            species=data['species'],
            species_other=data.get('species_other', ''),
            size=data['size'],
            sex=data['sex'],
            age=data['age'],
            weight=data['weight'],
            color=data['color'],
        )

        cover_index = data.get('cover_index', 0)
        for idx, image_file in enumerate(image_files):
            self.repo.add_image(pet, image_file, is_cover=(idx == cover_index))

        app_config.log_info(f'Pet criado: {pet.name} (dono: {owner.email})')
        return pet

    def update_pet(self, pet_id: int, requesting_user, data: dict, image_files: list) -> Pet:
        """Atualiza pet. Somente o dono pode atualizar."""
        pet = self._get_and_authorize(pet_id, requesting_user)

        validator = PetCreationValidationStrategy()
        valid, message = validator.validate(data)
        if not valid:
            raise ValueError(message)

        pet.name = data['name']
        pet.species = data['species']
        pet.species_other = data.get('species_other', '')
        pet.size = data['size']
        pet.sex = data['sex']
        pet.age = data['age']
        pet.weight = data['weight']
        pet.color = data['color']

        delete_ids = data.get('delete_image_ids') or []
        remaining_after_delete = (
            pet.images.exclude(pk__in=delete_ids).count() if delete_ids else pet.images.count()
        )
        final_count = remaining_after_delete + len(image_files)
        if final_count > 4:
            raise ValueError('Você pode ter no máximo 4 fotos por pet.')
        if final_count == 0:
            raise ValueError('O pet precisa ter ao menos uma foto.')

        if delete_ids:
            self.repo.delete_images_by_ids(pet, delete_ids)

        new_images = [self.repo.add_image(pet, image_file, is_cover=False) for image_file in image_files]

        cover_existing_id = data.get('cover_existing_id')
        if cover_existing_id:
            self.repo.set_cover(pet, cover_existing_id)
        elif new_images:
            cover_index = data.get('cover_index', 0)
            if 0 <= cover_index < len(new_images):
                self.repo.set_cover(pet, new_images[cover_index].id)
        elif delete_ids and not pet.images.filter(is_cover=True).exists():
            first = pet.images.order_by('id').first()
            if first:
                self.repo.set_cover(pet, first.id)

        self.repo.save(pet)
        return pet

    def delete_pet(self, pet_id: int, requesting_user) -> None:
        """Remove pet e suas imagens. Somente o dono pode remover."""
        pet = self._get_and_authorize(pet_id, requesting_user)
        self.repo.delete_images(pet)
        self.repo.delete(pet)
        app_config.log_info(f'Pet removido: id={pet_id}')

    def schedule_visit(self, pet_id: int, requesting_user) -> dict:
        """Agenda visita de adoção. Aplica regras de negócio do domínio."""
        pet = self.repo.get_by_id(pet_id)
        if not pet:
            raise LookupError('Pet não encontrado!')

        # Regra 1: não pode agendar visita no próprio pet
        if pet.owner_id == requesting_user.pk:
            raise PermissionError('Não é permitido agendar visita para o seu próprio Pet!')

        # Regra 2: não pode agendar duas vezes o mesmo pet
        if pet.adopter_id == requesting_user.pk:
            raise PermissionError('Você já agendou uma visita para este Pet!')

        pet.adopter = requesting_user
        self.repo.save(pet)

        self.notifications.notify(
            pet.owner,
            f'{requesting_user.name} agendou uma visita para adotar {pet.name}.',
            pet=pet,
        )

        app_config.log_info(f'Visita agendada: pet={pet_id}, adotante={requesting_user.email}')
        return {
            'message': (
                f'A visita foi agendada com sucesso, entre em contato com '
                f'{pet.owner.name} pelo telefone {pet.owner.phone}'
            )
        }

    def conclude_adoption(self, pet_id: int, requesting_user) -> dict:
        """Conclui o ciclo de adoção. Somente o dono pode concluir.

        Transfere a posse do pet para o adotante: ele passa a ser o novo
        dono e some da lista de pets do dono anterior.
        """
        pet = self._get_and_authorize(pet_id, requesting_user)
        if not pet.adopter_id:
            raise ValueError('Não há adotante agendado para concluir a adoção.')

        adopter = pet.adopter
        pet.available = False
        pet.owner = pet.adopter
        self.repo.save(pet)

        self.notifications.notify(
            adopter,
            f'Sua solicitação de adoção de {pet.name} foi aceita! Parabéns.',
            pet=pet,
        )

        app_config.log_info(f'Adoção concluída: pet={pet_id}, novo dono={adopter.email}')
        return {'message': 'Parabéns! O ciclo de adoção foi finalizado com sucesso!'}

    def deny_adoption(self, pet_id: int, requesting_user) -> dict:
        """Nega a solicitação de adoção agendada. Somente o dono pode negar.

        Remove o adotante agendado e mantém o pet disponível, para que o
        dono continue procurando outro interessado.
        """
        pet = self._get_and_authorize(pet_id, requesting_user)
        if not pet.adopter_id:
            raise ValueError('Não há adotante agendado para negar.')

        denied_adopter = pet.adopter
        pet.adopter = None
        self.repo.save(pet)

        self.notifications.notify(
            denied_adopter,
            f'Sua solicitação de adoção de {pet.name} foi negada pelo dono.',
            pet=pet,
        )

        app_config.log_info(f'Adoção negada: pet={pet_id}')
        return {'message': 'Solicitação de adoção negada. O pet continua disponível para adoção.'}

    # --- Auxiliares privados ---

    def _get_and_authorize(self, pet_id: int, user) -> Pet:
        """Busca o pet e verifica que o usuário é o dono."""
        pet = self.repo.get_by_id(pet_id)
        if not pet:
            raise LookupError('Pet não encontrado!')
        if pet.owner_id != user.pk:
            raise PermissionError(
                'Houve um problema em processar a sua solicitação, tente novamente mais tarde!'
            )
        return pet
