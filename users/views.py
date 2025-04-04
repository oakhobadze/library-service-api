from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


@extend_schema(
    summary="Register a new user",
    description="Creates a new user account with the provided credentials.",
)
class RegisterView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="Retrieve or update user profile",
    description="Allows authenticated users to view or update their profile information.",
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the current user's profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the authenticated user"""
        return self.request.user

    @extend_schema(
        summary="Update user profile",
        description="Partially updates the authenticated user's profile."
    )
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
