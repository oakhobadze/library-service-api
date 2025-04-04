from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(
        summary="Get a list of books",
        description="Returns a list of all books in the database.",
    ),
    retrieve=extend_schema(
        summary="Get book details",
        description="Returns detailed information about a book by its ID.",
    ),
    create=extend_schema(
        summary="Create a new book",
        description="Creates a new book (only accessible to administrators).",
    ),
    update=extend_schema(
        summary="Update a book",
        description="Updates book details (only accessible to administrators).",
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Allows partial updates to book details (only accessible to administrators).",
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Deletes a book from the database (only accessible to administrators).",
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    """CRUD operations for books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
