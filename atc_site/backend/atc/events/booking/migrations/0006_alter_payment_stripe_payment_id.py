# Generated by Django 4.1.2 on 2024-04-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_payment_stripe_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='stripe_payment_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]