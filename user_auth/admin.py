from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from SGN.models import Estudante,Professor

from user_auth.forms import EstudanteRegistrationForm

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('nome', 'sobrenome', 'telefone', 'telefone2', 'endereco', 'sexo', 'img')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Datas Importantes'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff', 'type')
    search_fields = ('email', 'nome', 'sobrenome')
    ordering = ('email',)


class EstudanteAdmin(UserAdmin):
    form = EstudanteRegistrationForm
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.ESTUDANTE)

    def save_model(self, request, obj, form, change):
        obj.type = User.Type.ESTUDANTE
        obj.save()


class ProfessorAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=User.Type.PROFESSOR)

    def save_model(self, request, obj, form, change):
        obj.type = User.Type.PROFESSOR
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(Estudante, EstudanteAdmin)
admin.site.register(Professor, ProfessorAdmin)