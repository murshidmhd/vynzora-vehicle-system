from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter


class VehicleListCreateAPIView(APIView):
    serializer_class = VehicleSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "brand",
                str,
                OpenApiParameter.QUERY,
                description="Filterby vehicle brand",
            ),
            OpenApiParameter(
                "fuel_type",
                str,
                OpenApiParameter.QUERY,
                description="Filter by fuel type (Petrol, Diesel, Electric, Hybrid)",
            ),
            OpenApiParameter(
                "is_available",
                bool,
                OpenApiParameter.QUERY,
                description="Filter by availability (true/false)",
            ),
        ]
    )
    def get(self, request):
        queryset = Vehicle.objects.all()

        brand = request.query_params.get("brand")
        fuel_type = request.query_params.get("fuel_type")
        is_available = request.query_params.get("is_available")

        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        if fuel_type:
            queryset = queryset.filter(fuel_type__iexact=fuel_type)

        if is_available is not None:
            is_avail_bool = is_available.lower() in ["true", "1"]
            queryset = queryset.filter(is_available=is_avail_bool)

        serializer = VehicleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetailAPIView(APIView):
    serializer_class = VehicleSerializer

    def get_object(self, id):
        return get_object_or_404(Vehicle, id=id)

    def get(self, request, id):
        vehicle = self.get_object(id)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        vehicle = self.get_object(id)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        vehicle = self.get_object(id)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingListCreateAPIView(APIView):
    serializer_class = BookingSerializer

    def get(self, request):
        bookings = Booking.objects.select_related("vehicle").all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetailAPIView(APIView):
    serializer_class = BookingSerializer

    def get_object(self, id):
        return get_object_or_404(Booking.objects.select_related("vehicle"), id=id)

    def get(self, request, id):
        booking = self.get_object(id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
