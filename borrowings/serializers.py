from rest_framework import serializers
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ("borrow_date", "actual_return_date")

    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.book.inventory -= 1
        borrowing.book.save()
        return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(required=True)

    class Meta:
        model = Borrowing
        fields = ['id', 'book', 'user', 'borrow_date', 'expected_return_date', 'actual_return_date']
        read_only_fields = ['id', 'book', 'user', 'borrow_date', 'expected_return_date']

    def update(self, instance, validated_data):
        instance.actual_return_date = validated_data.get('actual_return_date', instance.actual_return_date)
        instance.save()

        instance.book.inventory += 1
        instance.book.save()

        return instance
