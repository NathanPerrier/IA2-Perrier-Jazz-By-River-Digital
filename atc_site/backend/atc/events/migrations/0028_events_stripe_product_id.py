# Generated by Django 4.1.2 on 2024-05-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_eventvoucher_stripe_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]