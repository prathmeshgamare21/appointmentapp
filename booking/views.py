from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Barbershop, Barber, Service, Customer, Appointment
from .forms import AppointmentForm, CustomerRegistrationForm
import json


def home(request):
    """Home page displaying all barbershops"""
    barbershops = Barbershop.objects.all()
    return render(request, 'booking/home.html', {'barbershops': barbershops})


def barbershop_detail(request, barbershop_id):
    """Display barbershop details with services and barbers"""
    barbershop = get_object_or_404(Barbershop, id=barbershop_id)
    services = barbershop.services.all()
    barbers = barbershop.barbers.filter(is_available=True)
    return render(request, 'booking/barbershop_detail.html', {
        'barbershop': barbershop,
        'services': services,
        'barbers': barbers
    })


@login_required
def book_appointment(request, barbershop_id):
    """Book an appointment at a specific barbershop"""
    barbershop = get_object_or_404(Barbershop, id=barbershop_id)
    services = barbershop.services.all()
    barbers = barbershop.barbers.filter(is_available=True)
    
    # Get or create customer profile
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={'phone_number': ''}
    )
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, barbershop=barbershop)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm(barbershop=barbershop)
    
    return render(request, 'booking/book_appointment.html', {
        'form': form,
        'barbershop': barbershop,
        'services': services,
        'barbers': barbers,
        'customer': customer
    })


def get_available_times(request, barber_id, date):
    """AJAX endpoint to get available appointment times for a barber on a specific date"""
    try:
        barber = get_object_or_404(Barber, id=barber_id)
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Get barbershop hours
        barbershop = barber.barbershop
        opening_time = barbershop.opening_time
        closing_time = barbershop.closing_time
        
        # Generate time slots (30-minute intervals)
        available_times = []
        current_time = datetime.combine(appointment_date, opening_time)
        end_time = datetime.combine(appointment_date, closing_time)
        
        while current_time < end_time:
            time_slot = current_time.time()
            
            # Check if this time slot is already booked
            is_booked = Appointment.objects.filter(
                barber=barber,
                appointment_date=appointment_date,
                appointment_time=time_slot,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if not is_booked:
                available_times.append(time_slot.strftime('%H:%M'))
            
            current_time += timedelta(minutes=30)
        
        return JsonResponse({'available_times': available_times})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def appointment_confirmation(request, appointment_id):
    """Display appointment confirmation"""
    appointment = get_object_or_404(Appointment, id=appointment_id, customer__user=request.user)
    return render(request, 'booking/appointment_confirmation.html', {'appointment': appointment})


@login_required
def my_appointments(request):
    """Display user's appointments"""
    try:
        customer = Customer.objects.get(user=request.user)
        appointments = customer.appointments.all().order_by('-appointment_date', '-appointment_time')
    except Customer.DoesNotExist:
        appointments = []
    
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})


@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, customer__user=request.user)
    
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this appointment.')
    
    return redirect('my_appointments')


def register_customer(request):
    """Customer registration"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data.get('date_of_birth')
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our barbershop booking system.')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
