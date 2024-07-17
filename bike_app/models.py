from main_app.models import User
from django.db import models


class Bike(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BikeRental(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    rental_start_time = models.DateTimeField(auto_now_add=True)
    rental_end_time = models.DateTimeField(null=True, blank=True)
    rental_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.bike.name} - {self.rental_start_time}"

    def calculate_rental_cost(self):
        if self.rental_end_time:
            duration = (self.rental_end_time - self.rental_start_time).total_seconds() / 3600
            hourly_rate = 5
            return duration * hourly_rate
        return 0
