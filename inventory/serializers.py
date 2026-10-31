import re
from datetime import date
from rest_framework import serializers
from .models import Vehicle, Booking


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["total_amount", "created_at"]

    def validate_customer_phone(self, value):
        """Rule 5: Phone number must be exactly 10 digits."""
        cleaned_phone = value.strip()
        if not (cleaned_phone.isdigit() and len(cleaned_phone) == 10):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return cleaned_phone

    def validate(self, attrs):
        vehicle = attrs.get("vehicle")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        today = date.today()

        if start_date and start_date < today:
            raise serializers.ValidationError(
                {"start_date": "Start date cannot be in the past."}
            )

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be strictly after the start date"}
            )
        if vehicle and not vehicle.is_available and not self.instance:
            raise serializers.ValidationError(
                {"vehicle": f"The vehicle '{vehicle.name}' is currently unavailable"}
            )

        if vehicle and start_date and end_date:
            overlapping_bookings = Booking.objects.filter(
                vehicle=vehicle, start_date__lte=end_date, end_date__gte=start_date
            )

            # If updating an existing booking, don't conflict with yourself!
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    {
                        "non_field_errors": [
                            f"Vehicle '{vehicle.name}' is already booked forthese dates."
                        ]
                    }
                )

        return attrs

    def create(self, validated_data):
        """Rule 2: Auto-calculate total_amount and update vehicle
        availability."""
        vehicle = validated_data["vehicle"]
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        # 1. Calculate duration in days
        rental_days = (end_date - start_date).days

        # 2. Calculate total price: days * price_per_day
        total_price = rental_days * vehicle.price_per_day
        validated_data["total_amount"] = total_price

        # 3. Create and save the booking record
        booking = super().create(validated_data)

        # 4. Rule: After booking, vehicle becomes unavailable
        vehicle.is_available = False
        vehicle.save(update_fields=["is_available"])

        return booking
