from django.urls import path
from .views import BorrowingListCreateView, BorrowingDetailView, BorrowingReturnView

urlpatterns = [
    path("borrowings/", BorrowingListCreateView.as_view(), name="borrowings-list-create"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowings-detail"),
    path("borrowings/<int:pk>/return/", BorrowingReturnView.as_view(), name="borrowings-return"),
]

app_name = "borrowings"
