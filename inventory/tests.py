from rest_framework import status
from datetime import date, timedelta
from .models import Booking, Vehicle

from rest_framework.test import APITestCase


class VehicleBookingAPITests(APITestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name="Innova Crysta",
            brand="Toyota",
            year=2023,
            price_per_day=1500.00,
            fuel_type="Diesel",
            is_available=True,
        )

    def test_booking_rejects_past_start_date(self):
        """Rule 3: Start date cannot be in the past."""
        yesterday = date.today() - timedelta(days=1)
        end = date.today() + timedelta(days=3)

        payload = {
            "vehicle": self.vehicle.id,
            "customer_name": "Test User",
            "customer_phone": "9876543210",
            "start_date": yesterday.isoformat(),
            "end_date": end.isoformat(),
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_date", response.data)

    def test_booking_rejects_end_date_before_start_date(self):
        """Rule 4: End date must be after start date."""
        today = date.today()
        payload = {
            "vehicle": self.vehicle.id,
            "customer_name": "Test User",
            "customer_phone": "9876543210",
            "start_date": (today + timedelta(days=5)).isoformat(),
            "end_date": (
                today + timedelta(days=2)
            ).isoformat(),  # Invalid: end before start!
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("end_date", response.data)

    def test_booking_rejects_invalid_phone(self):
        """Rule 5: Phone number must be 10 digits."""
        today = date.today()
        payload = {
            "vehicle": self.vehicle.id,
            "customer_name": "Test User",
            "customer_phone": "12345",  # Invalid: only 5 digits!
            "start_date": (today + timedelta(days=1)).isoformat(),
            "end_date": (today + timedelta(days=3)).isoformat(),
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_phone", response.data)

    def test_double_booking_overlap_prevention(self):
        """Rule 1: Vehicle cannot be double-booked for overlapping
        dates."""
        today = date.today()
        start_1 = today + timedelta(days=10)
        end_1 = today + timedelta(days=15)

        # 1. First booking succeeds
        Booking.objects.create(
            vehicle=self.vehicle,
            customer_name="First Customer",
            customer_phone="9876543210",
            start_date=start_1,
            end_date=end_1,
            total_amount=7500.00,
        )

        # 2. Second booking attempts to book during overlapping dates(days 12 to 14)
        payload = {
            "vehicle": self.vehicle.id,
            "customer_name": "Second Customer",
            "customer_phone": "9123456780",
            "start_date": (today + timedelta(days=12)).isoformat(),
            "end_date": (today + timedelta(days=14)).isoformat(),
        }
        response = self.client.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
