# Generated by Django 4.1.2 on 2024-05-04 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_voucher_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventvoucher',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]