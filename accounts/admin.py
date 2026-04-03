from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("phone", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("phone", "first_name", "last_name", "email")
    ordering = ("phone",)

    fieldsets = UserAdmin.fieldsets + (
        ("Contact", {"fields": ("phone", "address")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Contact", {"fields": ("phone", "address")}),
    )
