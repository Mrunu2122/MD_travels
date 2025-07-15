import json
from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages

from .models import Trip, DailySummary, DailyExpense
from .forms import TripForm, DailySummaryForm, DailyExpenseForm


def home(request):
    selected_date = request.GET.get('date')
    selected_date = date.fromisoformat(selected_date) if selected_date else date.today()

    # Trips & Summary
    trips = Trip.objects.filter(date=selected_date)
    summary = DailySummary.objects.filter(date=selected_date).first()
    expense = DailyExpense.objects.filter(date=selected_date).first()

    # Earnings & Counts
    trip_earnings = trips.aggregate(Sum('fare'))['fare__sum'] or 0
    trip_count = trips.count()

    summary_earnings = summary.total_earnings() if summary else 0
    summary_count = summary.total_trips() if summary else 0

    # Expenses
    expense_total = expense.total_expense() if expense else 0

    # Final Daily Totals
    total_earnings = (trip_earnings + summary_earnings) - expense_total
    total_trips = trip_count + summary_count

    # WhatsApp message
    whatsapp_text = (
        f"MD Travels | {selected_date.strftime('%d %B %Y')}\n"
        f"Trips Completed: {total_trips}\n"
        f"Total Earnings: ₹{total_earnings}"
    )

    # Weekly chart data
    today = date.today()
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_data = []
    for d in week_dates:
        trip_sum = Trip.objects.filter(date=d).aggregate(Sum('fare'))['fare__sum'] or 0
        summary = DailySummary.objects.filter(date=d).first()
        expense = DailyExpense.objects.filter(date=d).first()
        total = trip_sum + (summary.total_earnings() if summary else 0) - (expense.total_expense() if expense else 0)
        weekly_data.append({'date': d.strftime('%a'), 'total': float(total)})

    # Monthly chart data
    month_dates = [today - timedelta(days=i) for i in range(29, -1, -1)]
    monthly_data = []
    for d in month_dates:
        trip_sum = Trip.objects.filter(date=d).aggregate(Sum('fare'))['fare__sum'] or 0
        summary = DailySummary.objects.filter(date=d).first()
        expense = DailyExpense.objects.filter(date=d).first()
        total = trip_sum + (summary.total_earnings() if summary else 0) - (expense.total_expense() if expense else 0)
        monthly_data.append({'date': d.strftime('%d %b'), 'total': float(total)})

    context = {
    'trips': trips,
    'total_earnings': total_earnings,
    'total_trips': total_trips,
    'trip_earnings': trip_earnings + summary_earnings,  # full earnings before expense
    'expense_total': expense_total,
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


# ✅ Daily Expense View
def daily_expenses_view(request):
    from decimal import Decimal, InvalidOperation

    try:
        selected_date = request.GET.get('date')
        selected_date = date.fromisoformat(selected_date) if selected_date else date.today()
    except ValueError:
        selected_date = date.today()

    instance = DailyExpense.objects.filter(date=selected_date).first()

    if request.method == 'POST':
        try:
            # Safely parse decimal values
            petrol_str = request.POST.get('petrol_cng_expense', '0') or '0'
            basic_str = request.POST.get('basic_expense', '0') or '0'

            petrol = Decimal(petrol_str)
            basic = Decimal(basic_str)

            if instance:
                instance.petrol_cng_expense += petrol
                instance.basic_expense += basic
                instance.save()
            else:
                DailyExpense.objects.create(
                    date=selected_date,
                    petrol_cng_expense=petrol,
                    basic_expense=basic
                )

            messages.success(request, "✅ Expenses added successfully!")
            return redirect('home')

        except (InvalidOperation, ValueError) as e:
            messages.error(request, "❌ Invalid input. Please enter valid numbers.")
            # Fall through to render form again

    # GET method or failed POST
    form = DailyExpenseForm(initial={'date': selected_date})
    existing_total = instance.total_expense() if instance else 0
    recent_expenses = DailyExpense.objects.order_by('-date')[:7]

    return render(request, 'travel/daily_expenses.html', {
        'form': form,
        'existing_total': existing_total,
        'recent_expenses': recent_expenses,
    })
