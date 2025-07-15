from django.db import models

PLATFORM_CHOICES = [
    ('ola', 'Ola'),
    ('uber', 'Uber'),
    ('rapido', 'Rapido'),
]


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)

    def __str__(self):
        return f"{self.destination} - ₹{self.fare} ({self.platform})"


class DailyExpense(models.Model):
    date = models.DateField(unique=True)
    petrol_cng_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    basic_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def total_expense(self):
        return self.petrol_cng_expense + self.basic_expense

    def __str__(self):
        return f"{self.date} - ₹{self.total_expense()} total expense"


class DailySummary(models.Model):
    date = models.DateField(unique=True)
    hours_worked = models.FloatField(default=0)

    ola_trips = models.IntegerField(default=0)
    ola_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    uber_trips = models.IntegerField(default=0)
    uber_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    rapido_trips = models.IntegerField(default=0)
    rapido_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    manual_total_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Use this if you want to override and enter a total amount directly."
    )

    def total_trips(self):
        return self.ola_trips + self.uber_trips + self.rapido_trips

    def total_earnings(self):
        platform_total = self.ola_earnings + self.uber_earnings + self.rapido_earnings
        total_income = platform_total + self.manual_total_income

        # Subtract Daily Expenses
        try:
            expense = DailyExpense.objects.get(date=self.date)
            total_income -= expense.total_expense()
        except DailyExpense.DoesNotExist:
            pass

        return total_income

    def __str__(self):
        return f"{self.date} - ₹{self.total_earnings()} for {self.total_trips()} trips"
