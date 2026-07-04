"""
--- CAMADA: Views / Controllers (DRF) ---

ViewSets recebem a requisição HTTP, delegam ao PetService e retornam a resposta.
Nenhuma regra de negócio reside aqui.

Princípio S (SOLID): views responsáveis exclusivamente por I/O HTTP.
Princípio D (SOLID): dependem do PetService (abstração).
"""
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pets.repositories import PetRepository
from apps.pets.serializers import PetCreateSerializer, PetSerializer
from apps.pets.services import PetService


class PetListCreateView(APIView):
    """
    GET  /api/pets/         — Lista todos os pets (público).
    POST /api/pets/         — Cria um pet (autenticado).
    """

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        species = request.query_params.get('species') or None
        size = request.query_params.get('size') or None
        pets = PetRepository.get_all(species=species, size=size)
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response({'pets': serializer.data})

    def post(self, request):
        serializer = PetCreateSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'message': str(first_error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        images = request.FILES.getlist('images')
        service = PetService()
        try:
            pet = service.create_pet(request.user, serializer.validated_data, images)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        out = PetSerializer(pet, context={'request': request})
        return Response(
            {'message': 'Pet cadastrado com sucesso!', 'pet': out.data},
            status=status.HTTP_201_CREATED,
        )


class MyPetsView(APIView):
    """GET /api/pets/mypets/ — Lista os pets do usuário autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = PetRepository.get_by_owner(request.user)
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response({'pets': serializer.data})


class MyAdoptionsView(APIView):
    """GET /api/pets/myadoptions/ — Lista as adoções agendadas (ainda não concluídas)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = PetRepository.get_by_adopter(request.user)
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response({'pets': serializer.data})


class AdoptedPetsView(APIView):
    """GET /api/pets/adopted/ — Lista os pets que o usuário adotou de outra pessoa."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = PetRepository.get_adopted_by(request.user)
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response({'pets': serializer.data})


class GivenAwayPetsView(APIView):
    """GET /api/pets/given-away/ — Lista os pets cadastrados pelo usuário que foram adotados por outros."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = PetRepository.get_given_away_by(request.user)
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response({'pets': serializer.data})


class PetDetailView(APIView):
    """
    GET    /api/pets/<id>/  — Detalhes do pet (público).
    PATCH  /api/pets/<id>/  — Atualiza pet (somente dono).
    DELETE /api/pets/<id>/  — Remove pet (somente dono).
    """

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        pet = PetRepository.get_by_id(pk)
        if not pet:
            return Response({'message': 'Pet não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'pet': PetSerializer(pet, context={'request': request}).data})

    def patch(self, request, pk):
        serializer = PetCreateSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({'message': str(first_error)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        images = request.FILES.getlist('images')
        service = PetService()
        try:
            pet = service.update_pet(pk, request.user, serializer.validated_data, images)
        except LookupError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response({'message': 'Pet atualizado com sucesso!', 'pet': PetSerializer(pet, context={'request': request}).data})

    def delete(self, request, pk):
        service = PetService()
        try:
            service.delete_pet(pk, request.user)
        except LookupError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Pet removido com sucesso!'})


class ScheduleVisitView(APIView):
    """PATCH /api/pets/<id>/schedule/ — Agenda visita de adoção."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        service = PetService()
        try:
            result = service.schedule_visit(pk, request.user)
        except LookupError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(result)


class ConcludeAdoptionView(APIView):
    """PATCH /api/pets/<id>/conclude/ — Conclui o ciclo de adoção."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        service = PetService()
        try:
            result = service.conclude_adoption(pk, request.user)
        except LookupError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(result)


class DenyAdoptionView(APIView):
    """PATCH /api/pets/<id>/deny/ — Nega a solicitação de adoção agendada."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        service = PetService()
        try:
            result = service.deny_adoption(pk, request.user)
        except LookupError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as exc:
            return Response({'message': str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(result)
