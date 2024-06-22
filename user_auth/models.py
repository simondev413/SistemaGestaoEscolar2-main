from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Criptografar a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        PROFESSOR = 'professor', 'Professor'
        ESTUDANTE = 'estudante', 'Estudante'
    class Sexo(models.TextChoices):
        M='Masculino','Masculino'
        F='Feminino','Feminino'

    nome = models.CharField(max_length=60)
    sobrenome = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    telefone = models.CharField(max_length=20)
    telefone2 = models.CharField(max_length=20, verbose_name='Telefone 2 (Opcional)',null=True,blank=True)
    endereco = models.CharField(max_length=255)
    sexo = models.CharField(max_length=20, choices=Sexo.choices)
    img = models.FileField(upload_to='img/users/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.ADMIN)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'