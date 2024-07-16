import math

from django.db import models
from django.conf import settings
from django.utils import timezone


class Bike(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} rented {self.bike.name} at {self.start_time}"

    def calculated_cost(self):
        if self.end_time:
            duration = self.end_time - self.start_time
            hours = math.ceil(duration.total_seconds() / 3600)
            return hours
        return 0
