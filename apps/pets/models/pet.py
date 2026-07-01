"""
--- CAMADA: Models (Entidades ORM) ---

Pet e PetImage modelam o domínio de adoção com relacionamentos FK reais
entre tabelas SQL — sem objetos embutidos ou listas serializada em campos.

Princípio S (SOLID): cada classe modela uma única entidade do domínio.
"""
from django.conf import settings
from django.db import models


class Pet(models.Model):
    """Entidade Pet com FK para o dono (owner) e o adotante (adopter)."""

    name = models.CharField('Nome', max_length=100)
    age = models.CharField('Idade', max_length=50)        # ex: "3 anos"
    weight = models.CharField('Peso', max_length=50)      # ex: "5 kg"
    color = models.CharField('Cor', max_length=50)
    available = models.BooleanField('Disponível para adoção', default=True)

    # FK para o dono: ao deletar o dono, remove seus pets em cascata
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_pets',
        verbose_name='Dono',
    )

    # FK para o adotante: ao deletar o adotante, limpa a referência (SET_NULL)
    adopter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_adoptions',
        verbose_name='Adotante',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} (dono: {self.owner.name})'


class PetImage(models.Model):
    """Imagem de um Pet — relação 1:N (um pet pode ter várias fotos)."""

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Pet',
    )
    image = models.ImageField('Imagem', upload_to='pets/')

    class Meta:
        verbose_name = 'Imagem do Pet'
        verbose_name_plural = 'Imagens do Pet'

    def __str__(self) -> str:
        return f'Imagem de {self.pet.name}'
