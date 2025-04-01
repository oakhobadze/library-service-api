from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverType.choices)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    def __str__(self):
        return f"{self.title} by {self.author}"
