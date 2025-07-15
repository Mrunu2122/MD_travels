from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_trip, name='add_trip'),
    path('quick-entry/', views.quick_entry, name='quick_entry'),
    path('daily-expenses/', views.daily_expenses_view, name='daily_expenses'),
]
