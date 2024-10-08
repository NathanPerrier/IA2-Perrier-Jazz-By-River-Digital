# Generated by Django 4.1.2 on 2024-04-04 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='tickets',
            new_name='ticket',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_response',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_response_code',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_response_message',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_response_raw',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_response_time',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='gateway_transaction_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_response',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_response_code',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_response_message',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_response_raw',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_response_time',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='method_transaction_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_details',
        ),
        migrations.AddField(
            model_name='payment',
            name='item',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
    ]
