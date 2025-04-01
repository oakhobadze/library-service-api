from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingReturnSerializer


class BorrowingListCreateView(generics.ListCreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active is not None:
            queryset = queryset.filter(actual_return_date__isnull=(is_active.lower() == "true"))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]


class BorrowingReturnView(generics.UpdateAPIView):
    serializer_class = BorrowingReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Borrowing,
            pk=self.kwargs['pk'],
            user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            borrowing,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            borrowing.book.inventory += 1
            borrowing.book.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
