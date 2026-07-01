from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'phone', 'is_staff', 'date_joined')
    search_fields = ('email', 'name', 'phone')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Dados adicionais', {'fields': ('name', 'phone', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados adicionais', {'fields': ('name', 'phone', 'image')}),
    )
