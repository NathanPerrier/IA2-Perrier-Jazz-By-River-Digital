# Generated by Django 4.1.2 on 2024-04-07 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_bookingvouchers_bookingfoodanddrinks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='food_and_drinks',
        ),
        migrations.RemoveField(
            model_name='events',
            name='vouchers',
        ),
    ]