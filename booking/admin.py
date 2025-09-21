from django.contrib import admin
from .models import Barbershop, Barber, Service, Customer, Appointment


@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email', 'opening_time', 'closing_time']
    list_filter = ['created_at']
    search_fields = ['name', 'address', 'email']


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ['user', 'barbershop', 'experience_years', 'is_available']
    list_filter = ['barbershop', 'is_available', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'specialties']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'barbershop', 'duration_minutes', 'price']
    list_filter = ['barbershop', 'duration_minutes']
    search_fields = ['name', 'description']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'date_of_birth']
    search_fields = ['user__first_name', 'user__last_name', 'phone_number']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'barber', 'service', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date', 'barber__barbershop']
    search_fields = ['customer__user__first_name', 'customer__user__last_name', 'barber__user__first_name']
    date_hierarchy = 'appointment_date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer__user', 'barber__user', 'service')
