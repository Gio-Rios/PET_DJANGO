"""Backfill: pets cadastrados antes do campo 'species' existir são cachorros.

Todos os pets já cadastrados até aqui são cães; o campo species foi
adicionado com default 'outro', então esta migration corrige o dado
real para 'cachorro' nesses registros legados.
"""
from django.db import migrations


def set_legacy_pets_as_dog(apps, schema_editor):
    Pet = apps.get_model('pets', 'Pet')
    Pet.objects.filter(species='outro', species_other='').update(species='cachorro')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0005_pet_size_pet_species_pet_species_other'),
    ]

    operations = [
        migrations.RunPython(set_legacy_pets_as_dog, noop),
    ]
