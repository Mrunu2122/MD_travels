from django import forms
from .models import Trip, DailySummary

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'fare', 'date', 'platform']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter destination'
            }),
            'fare': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fare'
            }),
            'platform': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = [
            'date', 'hours_worked',
            'ola_trips', 'ola_earnings',
            'uber_trips', 'uber_earnings',
            'rapido_trips', 'rapido_earnings',
            'manual_total_income',  # ✅ added this line
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'hours_worked': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hours worked today'
            }),
            'ola_trips': forms.NumberInput(attrs={'class': 'form-control'}),
            'ola_earnings': forms.NumberInput(attrs={'class': 'form-control'}),
            'uber_trips': forms.NumberInput(attrs={'class': 'form-control'}),
            'uber_earnings': forms.NumberInput(attrs={'class': 'form-control'}),
            'rapido_trips': forms.NumberInput(attrs={'class': 'form-control'}),
            'rapido_earnings': forms.NumberInput(attrs={'class': 'form-control'}),
            'manual_total_income': forms.NumberInput(attrs={  # ✅ widget for manual income
                'class': 'form-control',
                'placeholder': 'Any other extra income?'
            }),
        }
