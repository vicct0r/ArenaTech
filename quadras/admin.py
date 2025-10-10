from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'name', 'modified', 'is_active']
    search_fields = ['created_at', 'name', 'is_active']


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'modified', 'is_active', 'name', 'week_days_open', 'opening_time', 'closing_time']
    search_fields = ['created_at', 'is_active', 'name', 'opening_time', 'closing_time']


@admin.register(models.Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'modified', 'is_active', 'name', 'description', 'category', 'schedule', 'status', 'price']
    search_fields = ['created_at', 'modified', 'is_active', 'name', 'category', 'status']


@admin.register(models.ScheduleException)
class ScheduleExceptionAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'modified', 'is_active', 'name', 'description', 'start_time', 'end_time', 'is_closed']
    search_fields = ['start_time', 'end_time', 'is_active', 'is_closed']


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'court', 'start_time', 'end_time', 'status']
    search_fields = ['customer', 'court', 'start_time', 'end_time', 'status']