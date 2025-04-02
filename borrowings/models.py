from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from books.models import Book
from users.models import User


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    def clean(self):
        """ Проверка корректности дат перед сохранением """
        today = now().date()

        if self.borrow_date and self.borrow_date < today:
            raise ValidationError({"borrow_date": "Borrow date cannot be in the past."})

        if self.expected_return_date and self.borrow_date and self.expected_return_date < self.borrow_date:
            raise ValidationError({"expected_return_date": "Expected return date must be the same or after borrow date."})

        if self.actual_return_date and self.borrow_date and self.actual_return_date < self.borrow_date:
            raise ValidationError({"actual_return_date": "Actual return date must be the same or after borrow date."})

    def save(self, *args, **kwargs):
        """ Вызов валидации перед сохранением """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title}"
