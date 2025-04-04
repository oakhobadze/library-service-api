from datetime import datetime

from rest_framework import serializers
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "user", "borrow_date", "expected_return_date", "actual_return_date")
        read_only_fields = ("id", "actual_return_date")


    def validate_borrow_date(self, value):
        from django.utils.timezone import now
        if value < now().date():
            raise serializers.ValidationError("Borrow date cannot be in the past.")
        return value

    def validate_expected_return_date(self, value):
        borrow_date = self.initial_data.get("borrow_date")
        if isinstance(borrow_date, str):
            borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d").date()

        if value < borrow_date:
            raise serializers.ValidationError("Expected return date must be the same or after borrow date.")
        return value

    def create(self, validated_data):
        book = validated_data["book"]

        if book.inventory <= 0:
            raise serializers.ValidationError("This book is not available for borrowing.")

        book.inventory -= 1
        book.save()

        return super().create(validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(required=True)

    class Meta:
        model = Borrowing
        fields = ["id", "book", "user", "borrow_date", "expected_return_date", "actual_return_date"]
        read_only_fields = ["id", "book", "user", "borrow_date", "expected_return_date"]

    def validate_actual_return_date(self, value):
        from django.utils.timezone import now
        if value < now().date():
            raise serializers.ValidationError("Return date cannot be in the past.")
        return value

    def update(self, instance, validated_data):
        if instance.actual_return_date is not None:
            raise serializers.ValidationError("This borrowing has already been returned.")

        actual_return_date = validated_data["actual_return_date"]

        if actual_return_date < instance.borrow_date:
            raise serializers.ValidationError("Return date cannot be earlier than borrow date.")

        instance.actual_return_date = actual_return_date

        instance.book.inventory += 1
        instance.book.save()

        instance.save()

        return instance


