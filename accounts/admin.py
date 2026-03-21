from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):

    model = AppUser

    list_display = ("email", "first_name", "last_name", "role", "is_staff", "get_groups")

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Groups"
