from django.contrib import admin

from apps.pets.models import Pet, PetImage


class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'size', 'sex', 'owner', 'available', 'adopter', 'created_at')
    list_filter = ('available', 'species', 'size', 'sex')
    search_fields = ('name', 'owner__name', 'owner__email')
    inlines = [PetImageInline]
    readonly_fields = ('created_at', 'updated_at')
