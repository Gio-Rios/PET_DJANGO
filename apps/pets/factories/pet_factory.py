"""
Padrão GoF: Factory — PetFactory
-----------------------------------
Centraliza a criação de instâncias de Pet, encapsulando os valores padrão
(available=True) e a associação com o dono.

Princípio S (SOLID): a factory apenas cria o objeto — regras de negócio
(validação, imagens) ficam no PetService.
"""
from apps.pets.models import Pet


class PetFactory:
    """Fábrica para criação de instâncias de Pet (Factory GoF)."""

    @staticmethod
    def create(
        *, owner, name: str, age: str, weight: str, color: str,
        species: str = Pet.SPECIES_DOG, size: str = Pet.SIZE_MEDIUM,
        sex: str = Pet.SEX_MALE,
    ) -> Pet:
        """Cria e persiste um Pet com available=True por padrão."""
        pet = Pet(
            owner=owner,
            original_owner=owner,
            name=name,
            species=species,
            size=size,
            sex=sex,
            age=age,
            weight=weight,
            color=color,
            available=True,
        )
        pet.save()
        return pet

    @staticmethod
    def build(
        *, owner, name: str, age: str, weight: str, color: str,
        species: str = Pet.SPECIES_DOG, size: str = Pet.SIZE_MEDIUM,
        sex: str = Pet.SEX_MALE,
    ) -> Pet:
        """Constrói um Pet em memória sem persistir (útil em testes)."""
        return Pet(
            owner=owner,
            original_owner=owner,
            name=name,
            species=species,
            size=size,
            sex=sex,
            age=age,
            weight=weight,
            color=color,
            available=True,
        )
