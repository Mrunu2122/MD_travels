import json
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages

from .models import Trip, DailySummary
from .forms import TripForm
from .forms import TripForm, DailySummaryForm


def home(request):
    selected_date = request.GET.get('date')
    selected_date = date.fromisoformat(selected_date) if selected_date else date.today()

    trips = Trip.objects.filter(date=selected_date)
    summary = DailySummary.objects.filter(date=selected_date).first()

    trip_earnings = trips.aggregate(Sum('fare'))['fare__sum'] or 0
    trip_count = trips.count()

    summary_earnings = summary.total_earnings if summary else 0
    summary_count = summary.trip_count if summary else 0

    total_earnings = trip_earnings + summary_earnings
    total_trips = trip_count + summary_count

    whatsapp_text = (
        f"MD Travels | {selected_date.strftime('%d %B %Y')}\n"
        f"Trips Completed: {total_trips}\n"
        f"Total Earnings: ₹{total_earnings}"
    )

    today = date.today()
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_data = []
    for d in week_dates:
        trip_sum = Trip.objects.filter(date=d).aggregate(Sum('fare'))['fare__sum'] or 0
        summary = DailySummary.objects.filter(date=d).first()
        total = trip_sum + (summary.total_earnings if summary else 0)
        weekly_data.append({'date': d.strftime('%a'), 'total': float(total)})

    month_dates = [today - timedelta(days=i) for i in range(29, -1, -1)]
    monthly_data = []
    for d in month_dates:
        trip_sum = Trip.objects.filter(date=d).aggregate(Sum('fare'))['fare__sum'] or 0
        summary = DailySummary.objects.filter(date=d).first()
        total = trip_sum + (summary.total_earnings if summary else 0)
        monthly_data.append({'date': d.strftime('%d %b'), 'total': float(total)})

    context = {
        'trips': trips,
        'total_earnings': total_earnings,
        'total_trips': total_trips,
        'selected_date': selected_date,
        'whatsapp_text': whatsapp_text,
        'weekly_labels': json.dumps([d['date'] for d in weekly_data]),
        'weekly_earnings': json.dumps([d['total'] for d in weekly_data]),
        'monthly_labels': json.dumps([d['date'] for d in monthly_data]),
        'monthly_earnings': json.dumps([d['total'] for d in monthly_data]),
        'today': selected_date,
    }

    return render(request, 'travel/home.html', context)


def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TripForm()
    return render(request, 'travel/add_trip.html', {'form': form})


def quick_entry(request):
    if request.method == 'POST':
        form = DailySummaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Daily summary added successfully!")
            return redirect('home')
    else:
        form = DailySummaryForm(initial={'date': date.today()})

    return render(request, 'travel/quick_entry.html', {'form': form})
