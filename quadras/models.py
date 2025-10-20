from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError

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
    """ Agenda que pode representar 1..N quadras """
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5
    DOMINGO = 6

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
    week_days_open = MultiSelectField(choices=DIAS_SEMANA_CHOICES, max_length=22, default=None)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"{self.name} | {self.opening_time} - {self.closing_time}"


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
    category = models.ForeignKey(Category, related_name='category_courts', on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, related_name='court_schedule', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=3, choices=QUADRA_STATUS_CHOICES, default=DISPONIVEL)
    image = StdImageField(upload_to='courts_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.status}"


class ScheduleException(Base):
    """ Exceção no funcionamento das quadras, permitindo declarar dias, intervalos e horarios de almoço """
    name = models.CharField('Exceção', max_length=70)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    courts = models.ManyToManyField(Court, related_name='court_exceptions')
    is_closed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.start_time} - {self.end_time}'


class Booking(Base):
    PENDING = 'pd'
    CONFIRMED = 'cf'
    ACTIVE = 'ac'
    COMPLETED = 'cm'
    CANCELLED = 'cn'
    EXPIRED = 'ex' 
    REFUNDED = 're'

    BOOKING_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Canceled'),
        (EXPIRED, 'Expired'),
        (REFUNDED, 'Refunded')
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    court = models.ForeignKey(Court, related_name='courts_rented', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=2, choices=BOOKING_STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Booking: {self.court} - {self.start_time}"
    
    class Meta:
        unique_together = ['court', 'start_time', 'end_time']
