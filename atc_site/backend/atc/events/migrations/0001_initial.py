# Generated by Django 4.1.2 on 2024-03-06 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventFoodAndDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=256)),
                ('date', models.DateTimeField()),
                ('time', models.TimeField()),
                ('available_tickets', models.IntegerField()),
                ('sold', models.IntegerField()),
                ('sale_release_date', models.DateTimeField()),
                ('sale_end_date', models.DateTimeField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/events/')),
                ('food_and_drinks', models.ManyToManyField(blank=True, to='events.eventfoodanddrinks')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventScheduleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('purchase_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_left', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('expiration_date', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoodAndDrinksItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stock', models.IntegerField(default=0)),
                ('quantity_sold', models.IntegerField(default=0)),
                ('discount', models.FloatField(blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoodAndDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
                ('item', models.ManyToManyField(to='events.foodanddrinksitem')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.voucher')),
            ],
        ),
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events')),
                ('event_item', models.ManyToManyField(to='events.eventscheduleitem')),
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.eventschedule'),
        ),
        migrations.AddField(
            model_name='events',
            name='vouchers',
            field=models.ManyToManyField(blank=True, to='events.eventvoucher'),
        ),
        migrations.AddField(
            model_name='eventfoodanddrinks',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AddField(
            model_name='eventfoodanddrinks',
            name='food_and_drinks_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.foodanddrinksitem'),
        ),
    ]