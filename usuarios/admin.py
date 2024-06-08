# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from usuarios.models import Perfil


@admin.register(Perfil)
class ProfileAdmin(admin.ModelAdmin):
    # Profile admin

    list_display = ("pk", "user", "verificado")
    list_display_links = ("pk", "user")
    search_fields = (
        "user__username", "user__email",
        "user__first_name", "user__last_name", "telefono"
    )
    list_filter = ("verificado", "fecha_creacion", "fecha_modificacion")
    fieldsets = (
        ("Profile", {"fields": ("user", "foto")}),
        ("Extra info", {"fields": (("telefono",), "biografia", "verificado")}),
        ("Metadata", {"fields": ("fecha_creacion", "fecha_modificacion")}))
    readonly_fields = ("fecha_creacion", "fecha_modificacion")
    ordering = ("-id",)


class ProfileInline(admin.StackedInline):
    # Conexión con el Profile admin (para User admin)
    model = Perfil
    can_delete = False
    verbose_name_plural = "perfiles"


class UserAdmin(BaseUserAdmin):
    # Agrega el Profile admin al User admin
    inlines = (ProfileInline,)
    list_display = ("id", "username", "display_groups")
    ordering = ("-id",)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
