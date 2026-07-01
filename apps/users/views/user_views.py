"""
--- CAMADA: Views / Controllers (DRF) ---

Views recebem requisições HTTP, delegam ao Service e retornam respostas.
Nenhuma lógica de negócio reside aqui.

Princípio S (SOLID): view é responsável apenas por I/O HTTP.
Princípio D (SOLID): depende do UserService (abstração), não do ORM.
"""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from apps.users.serializers.user_serializers import UserEditSerializer
from apps.users.services import UserService


def _get_tokens(user) -> dict:
    """Gera par de tokens JWT para o usuário."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    """POST /api/users/register/ — Registro de novo usuário."""

    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'message': str(first_error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        service = UserService()
        try:
            user = service.register(serializer.validated_data)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        tokens = _get_tokens(user)
        return Response(
            {'message': 'Usuário criado com sucesso!', 'user': UserSerializer(user, context={'request': request}).data, **tokens},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/users/login/ — Autenticação e geração de tokens JWT."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'message': str(first_error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # authenticate usa o backend padrão do Django (PBKDF2)
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {'message': 'Usuário ou senha inválidos!'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        tokens = _get_tokens(user)
        return Response(
            {'message': 'Login realizado com sucesso!', 'user': UserSerializer(user, context={'request': request}).data, **tokens},
            status=status.HTTP_200_OK,
        )


class CheckUserView(APIView):
    """GET /api/users/checkuser/ — Retorna o usuário autenticado ou null."""

    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user, context={'request': request}).data)
        return Response(None)


class UserDetailView(APIView):
    """GET /api/users/<id>/ — Detalhes públicos de um usuário."""

    permission_classes = [AllowAny]

    def get(self, request, pk):
        from apps.users.repositories import UserRepository
        user = UserRepository.get_by_id(pk)
        if not user:
            return Response({'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'user': UserSerializer(user, context={'request': request}).data})


class UserEditView(APIView):
    """PATCH /api/users/<id>/edit/ — Edição de perfil (somente dono)."""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def patch(self, request, pk):
        if request.user.pk != pk:
            return Response(
                {'message': 'Você não pode editar o perfil de outro usuário.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserEditSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'message': str(first_error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        image_file = request.FILES.get('image')
        service = UserService()
        try:
            user = service.edit_profile(request.user, serializer.validated_data, image_file)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(
            {'message': 'Usuário atualizado com sucesso!', 'user': UserSerializer(user, context={'request': request}).data}
        )
