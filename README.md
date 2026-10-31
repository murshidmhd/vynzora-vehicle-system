# Vehicle Inventory & Booking REST API

A production-ready Django REST Framework (DRF) backend for managing vehicle inventories and processing bookings with strict validation business rules and interactive OpenAPI 3.0 (Swagger) documentation.

Built for the technical assessment by Vynzora Pvt. Ltd.

---

## Tech Stack
- Framework: Python 3.12, Django 6.1, Django REST Framework (DRF)
- Database: SQLite (default) / PostgreSQL compatible
- Filtering: django-filter
- API Documentation: drf-spectacular (OpenAPI 3.0 & Swagger UI)
- Automated Testing: Django / DRF APITestCase
- Production Server: Gunicorn WSGI
- Cloud Hosting: Render

---

## Core Business Rules Implemented
1. Double Booking Prevention: A vehicle cannot be double-booked for overlapping date ranges. Evaluated via bidirectional overlap query.
2. Auto-Calculated Total Price: Calculated on the backend as (end_date - start_date).days * vehicle.price_per_day. Field is read-only.
3. Start Date Validation: Bookings cannot start in the past.
4. End Date Validation: The end date must be strictly after the start date.
5. Phone Validation: Customer phone number must be exactly 10 digits.
6. Auto-Status Update: Upon booking creation, the vehicle availability (is_available) automatically switches to False.

---

## Project Structure
```text
vynzora_task/
├── inventory/
│   ├── migrations/       # Database migrations
│   ├── models.py         # Vehicle and Booking models
│   ├── serializers.py    # DRF Serializers with custom validators
│   ├── views.py          # APIViews for Vehicle and Booking endpoints
│   ├── urls.py           # App routing with plural and singular aliases
│   └── tests.py          # Automated unit test suite
├── vehicle_system/
│   ├── settings.py       # Project settings and drf-spectacular configuration
│   ├── urls.py           # Root routing and Swagger UI endpoints
│   └── wsgi.py           # WSGI entry point for Gunicorn
├── .env.example          # Environment variable template
├── manage.py
├── requirements.txt      # Project dependencies
└── README.md
```

---

## Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/murshidmhd/vynzora_task.git
cd vynzora_task
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

### 5. Apply database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run automated test suite
```bash
python manage.py test inventory
```

### 7. Start the local server
```bash
python manage.py runserver
```

---

## API Endpoints

### 1. Interactive Swagger Documentation
- GET /api/docs/ - Interactive Swagger UI
- GET /api/schema/ - Raw OpenAPI 3.0 schema download

### 2. Vehicle Endpoints
- GET /api/vehicles/ - List all vehicles (supports query filtering)
  - Query parameters:
    - `?brand=Toyota` (case-insensitive search)
    - `?fuel_type=Diesel` (Options: Petrol, Diesel, Electric, Hybrid)
    - `?is_available=true` (Options: true, false)
- POST /api/vehicles/ - Create a new vehicle
- GET /api/vehicles/<id>/ - Retrieve a single vehicle
- PUT /api/vehicles/<id>/ - Update a vehicle
- DELETE /api/vehicles/<id>/ - Delete a vehicle

### 3. Booking Endpoints
- GET /api/bookings/ - List all bookings
- POST /api/bookings/ - Create a new booking
- GET /api/bookings/<id>/ - Retrieve a single booking

---

## Sample Request & Response Payloads

### 1. Create a Vehicle (POST /api/vehicles/)
Request Body:
```json
{
  "name": "Innova Crysta",
  "brand": "Toyota",
  "year": 2023,
  "price_per_day": "1500.00",
  "fuel_type": "Diesel",
  "is_available": true
}
```
Response (201 Created):
```json
{
  "id": 1,
  "name": "Innova Crysta",
  "brand": "Toyota",
  "year": 2023,
  "price_per_day": "1500.00",
  "fuel_type": "Diesel",
  "is_available": true,
  "created_at": "2026-10-31T11:00:00Z"
}
```

---

### 2. Create a Booking (POST /api/bookings/)
Request Body:
```json
{
  "vehicle": 1,
  "customer_name": "Muhammed Murshid",
  "customer_phone": "9876543210",
  "start_date": "2026-11-05",
  "end_date": "2026-11-08"
}
```
Response (201 Created):
```json
{
  "id": 1,
  "vehicle": 1,
  "customer_name": "Muhammed Murshid",
  "customer_phone": "9876543210",
  "start_date": "2026-11-05",
  "end_date": "2026-11-08",
  "total_amount": "4500.00",
  "created_at": "2026-10-31T11:05:00Z"
}
```
*(Total amount is automatically calculated: 3 days multiplied by 1500.00 per day = 4500.00)*

---

### 3. Overlapping Double Booking Rejection
Request Body (Attempting to book during conflicting dates):
```json
{
  "vehicle": 1,
  "customer_name": "Alex Smith",
  "customer_phone": "9123456780",
  "start_date": "2026-11-06",
  "end_date": "2026-11-07"
}
```
Response (400 Bad Request):
```json
{
  "non_field_errors": [
    "Vehicle 'Innova Crysta' is already booked for these dates."
  ]
}
```

---

### 4. Invalid Phone Number Rejection
Request Body:
```json
{
  "vehicle": 1,
  "customer_name": "Alex Smith",
  "customer_phone": "12345",
  "start_date": "2026-11-10",
  "end_date": "2026-11-12"
}
```
Response (400 Bad Request):
```json
{
  "customer_phone": [
    "Phone number must be exactly 10 digits."
  ]
}
```

---

## Author
Muhammed Murshid  
Full-Stack Python Developer  
Malappuram, Kerala, India  
GitHub: https://github.com/murshidmhd  
LinkedIn: https://www.linkedin.com/in/murshid70/
