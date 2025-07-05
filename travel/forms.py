from django import forms
from .models import Trip, DailySummary

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'fare', 'date']
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
        }

class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = ['date', 'trip_count', 'total_earnings']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'trip_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total number of trips'
            }),
            'total_earnings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total earnings for the day'
            }),
        }
