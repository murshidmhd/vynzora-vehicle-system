from django.urls import path
from .views import (
    VehicleDetailAPIView,
    VehicleListCreateAPIView,
    BookingDetailAPIView,
    BookingListCreateAPIView,
)

urlpatterns = [
    path("vehicles/", VehicleListCreateAPIView.as_view(), name="vehicle-list-create"),
    path("vehicles/<int:id>/", VehicleDetailAPIView.as_view(), name="vehicle-detail"),
    # Booking Endpoints
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("bookings/<int:id>/", BookingDetailAPIView.as_view(), name="booking-detail"),
]
