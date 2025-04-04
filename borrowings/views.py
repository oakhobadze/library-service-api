from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingReturnSerializer


@extend_schema(
    summary="List and create borrowings",
    description="Returns a list of borrowings with optional filters (`user_id`, `is_active`). Allows users to create new borrowings.",
)
class BorrowingListCreateView(generics.ListCreateAPIView):
    """Retrieve list of borrowings or create a new one"""
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter borrowings by user ID and active status"""
        queryset = Borrowing.objects.all()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            is_active = is_active.lower() == "true"
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        """Assign the current user to the borrowing record"""
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Retrieve borrowing details",
    description="Returns details of a specific borrowing by ID.",
)
class BorrowingDetailView(generics.RetrieveAPIView):
    """Retrieve a specific borrowing"""
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    summary="Return a borrowed book",
    description="Allows users to mark a book as returned. Only the user who borrowed the book can return it.",
)
class BorrowingReturnView(generics.UpdateAPIView):
    """Mark a book as returned"""
    serializer_class = BorrowingReturnSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve the borrowing object for the authenticated user"""
        return get_object_or_404(Borrowing, pk=self.kwargs['pk'], user=self.request.user)

    @extend_schema(
        summary="Get borrowing return details",
        description="Retrieve the borrowing record for return."
    )
    def get(self, request, *args, **kwargs):
        """Get borrowing details before returning"""
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

    @extend_schema(
        summary="Return a book",
        description="Marks a borrowed book as returned if not already returned."
    )
    def put(self, request, *args, **kwargs):
        """Mark the book as returned"""
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
            borrowing.book.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
