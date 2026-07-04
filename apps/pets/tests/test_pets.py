"""Testes de integração para os endpoints de pets e fluxo de adoção."""
import io

from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser


def make_test_image():
    """Cria um arquivo de imagem PNG válido em memória para testes."""
    img = Image.new('RGB', (100, 100), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.name = 'teste.png'
    buf.seek(0)
    return buf


def create_user(email, name='Usuário', phone='11999999999'):
    user = CustomUser.objects.create_user(
        username=email,
        email=email,
        password='senha123',
        name=name,
        phone=phone,
    )
    return user


class PetCRUDTests(APITestCase):
    """Testes de criação, listagem e detalhes de pets."""

    def setUp(self):
        self.owner = create_user('dono@exemplo.com', 'Dono do Pet')
        self.client.force_authenticate(user=self.owner)

    def test_create_pet_success(self):
        """Pet com dados válidos e imagem deve ser criado."""
        url = reverse('pet-list-create')
        payload = {
            'name': 'Rex',
            'species': 'cachorro',
            'size': 'medio',
            'sex': 'macho',
            'age': '3 anos',
            'weight': '10 kg',
            'color': 'Marrom',
        }
        img = make_test_image()
        payload['images'] = img
        response = self.client.post(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pet', response.data)

    def test_create_pet_missing_field(self):
        """Falta de campo obrigatório deve retornar 422."""
        url = reverse('pet-list-create')
        payload = {'name': 'Rex', 'age': '2 anos'}
        img = make_test_image()
        payload['images'] = img
        response = self.client.post(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_create_pet_without_image(self):
        """Pet sem imagem deve retornar 422."""
        url = reverse('pet-list-create')
        payload = {
            'name': 'Rex', 'species': 'cachorro', 'size': 'medio', 'sex': 'macho',
            'age': '3 anos', 'weight': '10 kg', 'color': 'Preto',
        }
        response = self.client.post(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_list_pets_public(self):
        """Listagem de pets deve ser pública (sem autenticação)."""
        self.client.force_authenticate(user=None)
        url = reverse('pet-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pets', response.data)


class AdoptionFlowTests(APITestCase):
    """Testes das regras de negócio do fluxo de adoção."""

    def setUp(self):
        self.owner = create_user('dono@exemplo.com', 'Dono')
        self.visitor = create_user('visitante@exemplo.com', 'Visitante')

        # Cria um pet para o owner
        from apps.pets.factories import PetFactory
        from apps.pets.repositories import PetRepository
        self.pet = PetFactory.create(
            owner=self.owner,
            name='Bolinha',
            age='2 anos',
            weight='5 kg',
            color='Branco',
        )

    def test_schedule_visit_success(self):
        """Visitante pode agendar visita em pet de outro usuário."""
        self.client.force_authenticate(user=self.visitor)
        url = reverse('pet-schedule', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_cannot_schedule_own_pet(self):
        """Dono não pode agendar visita no próprio pet."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('pet-schedule', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_cannot_schedule_twice(self):
        """Visitante não pode agendar o mesmo pet duas vezes."""
        self.client.force_authenticate(user=self.visitor)
        url = reverse('pet-schedule', kwargs={'pk': self.pet.pk})
        self.client.patch(url)  # primeiro agendamento
        response = self.client.patch(url)  # segundo agendamento
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_conclude_adoption_success(self):
        """Dono pode concluir adoção, marcando pet como indisponível."""
        self.client.force_authenticate(user=self.visitor)
        self.client.patch(reverse('pet-schedule', kwargs={'pk': self.pet.pk}))

        self.client.force_authenticate(user=self.owner)
        url = reverse('pet-conclude', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pet.refresh_from_db()
        self.assertFalse(self.pet.available)

    def test_only_owner_can_conclude(self):
        """Visitante não pode concluir adoção de pet alheio."""
        self.client.force_authenticate(user=self.visitor)
        url = reverse('pet-conclude', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_visit_success(self):
        """Adotante pode cancelar a visita agendada, liberando o pet."""
        self.client.force_authenticate(user=self.visitor)
        self.client.patch(reverse('pet-schedule', kwargs={'pk': self.pet.pk}))

        url = reverse('pet-cancel-visit', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pet.refresh_from_db()
        self.assertIsNone(self.pet.adopter)

    def test_cannot_cancel_visit_without_scheduling(self):
        """Usuário sem visita agendada não pode cancelar."""
        self.client.force_authenticate(user=self.visitor)
        url = reverse('pet-cancel-visit', kwargs={'pk': self.pet.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
