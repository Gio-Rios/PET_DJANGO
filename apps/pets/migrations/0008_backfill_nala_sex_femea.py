"""Backfill: a pet Nala é fêmea; os demais pets já cadastrados ficam machos
(valor default do campo sex cobre isso automaticamente).
"""
from django.db import migrations


def set_nala_as_female(apps, schema_editor):
    Pet = apps.get_model('pets', 'Pet')
    Pet.objects.filter(name__iexact='nala').update(sex='femea')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0007_pet_sex_alter_pet_species_alter_pet_species_other'),
    ]

    operations = [
        migrations.RunPython(set_nala_as_female, noop),
    ]
