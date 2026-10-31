from django.urls import path
from .views import (
    VehicleDetailAPIView,
    VehicleListCreateAPIView,
    BookingDetailAPIView,
    BookingListCreateAPIView,
)

urlpatterns = [
    # Vehicle Endpoints (plural as per spec, singular alias for convenience)
    path("vehicles/", VehicleListCreateAPIView.as_view(), name="vehicle-list-create"),
    path("vehicles/<int:id>/", VehicleDetailAPIView.as_view(), name="vehicle-detail"),
    path("vehicle/", VehicleListCreateAPIView.as_view(), name="vehicle-list-create-alt"),
    path("vehicle/<int:id>/", VehicleDetailAPIView.as_view(), name="vehicle-detail-alt"),

    # Booking Endpoints
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("bookings/<int:id>/", BookingDetailAPIView.as_view(), name="booking-detail"),
]
