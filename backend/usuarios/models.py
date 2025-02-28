from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O Email é obrigatório!')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O usuário precisa ativar "is_superuser"!')
        
        if extra_fields.get('is_staff', True) is not True:
            raise ValueError('O usuário precisa ativar "is_staff"!')
        
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField('Email', unique=True, max_length=100)
    telefone = models.CharField('Telefone', max_length=30)
    is_staff = models.BooleanField('Membro da Equipe', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone']
    objects = UsuarioManager()

    def __str__(self):
        return self.email
    