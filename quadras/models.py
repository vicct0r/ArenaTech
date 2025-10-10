from django.db import models
from django.db.models import Q

from stdimage import StdImageField
from multiselectfield import MultiSelectField


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Schedule(Base):
    """ Agenda base para quadras, podendo ser reaproveitada para mais de uma quadra """
    SEGUNDA = 'seg'
    TERCA = 'ter'
    QUARTA = 'qua'
    QUINTA = 'qui'
    SEXTA = 'sex'
    SABADO = 'sab'
    DOMINGO = 'dom'

    DIAS_SEMANA_CHOICES = (
        (SEGUNDA, 'Segunda-Feira'),
        (TERCA, 'Terça-Feira'),
        (QUARTA, 'Quarta-Feira'),
        (QUINTA, 'Quinta-Feira'),
        (SEXTA, 'Sexta-Feira'),
        (SABADO, 'Sábado'),
        (DOMINGO, 'Domingo')
    )

    name = models.CharField(max_length=100)
    week_days_open = MultiSelectField(choices=DIAS_SEMANA_CHOICES, max_length=3, default=None)
    opening_time = models.TimeField()
    closing_time = models.TimeField()


class Court(Base):
    DISPONIVEL = 'ds'
    OCUPADO = 'oc'
    RESERVADO = 'rs'
    MANUTENCAO = 'mn'
    FECHADO = 'fc'
    LIMPANDO = 'lp'

    QUADRA_STATUS_CHOICES = (
        (DISPONIVEL, 'Disponível'),
        (OCUPADO, 'Ocupado'),
        (RESERVADO, 'Reservado'),
        (MANUTENCAO, 'Manutenção'),
        (FECHADO, 'Fechado'),
        (LIMPANDO, 'Limpando')
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='courts', on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, related_name='court_schedule', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=3, choices=QUADRA_STATUS_CHOICES, default=DISPONIVEL)
    image = StdImageField(upload_to='courts_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ScheduleException(Base):
    """ Exceção no funcionamento das quadras, permitindo declarar dias, intervalos e horarios de almoço """
    name = models.CharField('Exceção', max_length=70)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    courts = models.ManyToManyField(Court)
    is_closed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.start_time} - {self.end_time}'