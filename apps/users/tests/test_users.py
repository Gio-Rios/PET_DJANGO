"""Testes de integração para os endpoints de usuários."""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser


class UserRegistrationTests(APITestCase):
    """Testes de registro de usuário."""

    def test_register_success(self):
        """Usuário válido deve ser criado com token JWT."""
        url = reverse('user-register')
        payload = {
            'name': 'João Silva',
            'email': 'joao@exemplo.com',
            'phone': '11999999999',
            'password': 'senha123',
            'confirmpassword': 'senha123',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertTrue(CustomUser.objects.filter(email='joao@exemplo.com').exists())

    def test_register_duplicate_email(self):
        """E-mail já cadastrado deve retornar 422."""
        CustomUser.objects.create_user(
            username='maria@exemplo.com',
            email='maria@exemplo.com',
            password='senha123',
            name='Maria',
            phone='11888888888',
        )
        url = reverse('user-register')
        payload = {
            'name': 'Maria Cópia',
            'email': 'maria@exemplo.com',
            'phone': '11777777777',
            'password': 'senha123',
            'confirmpassword': 'senha123',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('message', response.data)

    def test_register_password_mismatch(self):
        """Senhas diferentes devem retornar 422."""
        url = reverse('user-register')
        payload = {
            'name': 'Teste',
            'email': 'teste@exemplo.com',
            'phone': '11999999999',
            'password': 'senha123',
            'confirmpassword': 'outrasenha',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_register_missing_field(self):
        """Campo obrigatório faltando deve retornar 422."""
        url = reverse('user-register')
        payload = {
            'email': 'sem_nome@exemplo.com',
            'password': 'senha123',
            'confirmpassword': 'senha123',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserLoginTests(APITestCase):
    """Testes de login."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='teste@exemplo.com',
            email='teste@exemplo.com',
            password='senha123',
            name='Usuário Teste',
            phone='11999999999',
        )

    def test_login_success(self):
        """Credenciais válidas devem retornar tokens JWT."""
        url = reverse('user-login')
        response = self.client.post(url, {'email': 'teste@exemplo.com', 'password': 'senha123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        """Senha errada deve retornar 422."""
        url = reverse('user-login')
        response = self.client.post(url, {'email': 'teste@exemplo.com', 'password': 'errada'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_login_unknown_email(self):
        """E-mail não cadastrado deve retornar 422."""
        url = reverse('user-login')
        response = self.client.post(url, {'email': 'nao_existe@exemplo.com', 'password': 'senha123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
