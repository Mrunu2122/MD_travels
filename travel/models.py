from django.db import models


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

class DailySummary(models.Model):
    date = models.DateField(unique=True)
    trip_count = models.IntegerField()
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - ₹{self.total_earnings} for {self.trip_count} trips"

