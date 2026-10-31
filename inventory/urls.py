from django.urls import path
from .views import (
    VehicleDetailAPIView,
    VehicleListCreateAPIView,
    BokkingDetailAPIView,
    BookingListCreateAPIView,
)

urlpatterns = [
    path("vehicle/", VehicleListCreateAPIView.as_view(), name="vehicle-list-create"),
    path("vehicle/<int:id>/", VehicleDetailAPIView.as_view(), name="vehicle-detail"),
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("bookings/<int:id>/", BokkingDetailAPIView.as_view(), name="booking-detail"),
]
