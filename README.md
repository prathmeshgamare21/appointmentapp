# BarberBook — Barbershop Appointment Booking (Django)

A full-stack Django app for booking barbershop appointments with a clean, modern HTML/CSS (Bootstrap) frontend.

## Features
- Browse partner barbershops and view details
- List services and barbers per barbershop
- Customer registration/login/password reset
- Book appointments with real-time available time slots
- View and cancel your appointments
- Admin interface for managing barbershops, barbers, services, and appointments

## Tech Stack
- Backend: Django 4.2 (Python)
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite (default)

## Project Structure
```
MARK42/
├─ manage.py
├─ barbershop_booking/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ booking/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ urls.py
│  └─ views.py
├─ templates/
│  ├─ base.html
│  ├─ booking/
│  │  ├─ home.html
│  │  ├─ barbershop_detail.html
│  │  ├─ book_appointment.html
│  │  ├─ appointment_confirmation.html
│  │  └─ my_appointments.html
│  └─ registration/
│     ├─ login.html
│     ├─ register.html
│     ├─ password_reset.html
│     ├─ password_reset_done.html
│     ├─ password_reset_confirm.html
│     └─ password_reset_complete.html
├─ static/
│  └─ css/
│     └─ style.css
└─ requirements.txt
```

## Setup (Windows PowerShell)
1) Create and activate a virtual environment
```
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Make and apply migrations
```
py manage.py makemigrations
py manage.py migrate
```

4) Create a superuser to access the admin
```
py manage.py createsuperuser
```

5) Run the development server
```
py manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

- Admin panel: http://127.0.0.1:8000/admin/
- Login/Registration available via navbar

## Seeding Data (via Admin)
1) Log in to `/admin` with your superuser
2) Create a `Barbershop` (with opening/closing times)
3) Create `Service` items for that barbershop
4) Create `Barber` users:
   - First, create a `User` in admin
   - Then create a `Barber` and link to the user and barbershop

Customers are created automatically when a logged-in user books for the first time or registers through the app.

## Notes
- Email sending uses Django's console backend in development. Password reset links will appear in the terminal where `runserver` is running.
- Static files are served by Django in development mode.

## Next Improvements (Ideas)
- Barber schedules and holidays
- Prevent overlapping appointments using service duration
- Payment integration
- Barber ratings and reviews
- Multi-tenant support for many shops
