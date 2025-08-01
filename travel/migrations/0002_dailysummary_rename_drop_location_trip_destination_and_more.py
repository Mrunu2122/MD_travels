# Generated by Django 5.2.4 on 2025-07-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailySummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('total_trips', models.PositiveIntegerField()),
                ('total_earnings', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='drop_location',
            new_name='destination',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='pickup_location',
        ),
        migrations.AlterField(
            model_name='trip',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='fare',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
