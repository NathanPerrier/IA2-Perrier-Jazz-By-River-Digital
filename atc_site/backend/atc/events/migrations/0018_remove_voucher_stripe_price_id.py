# Generated by Django 4.1.2 on 2024-04-08 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_eventvoucher_stripe_price_id_voucher_stripe_price_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher',
            name='stripe_price_id',
        ),
    ]
