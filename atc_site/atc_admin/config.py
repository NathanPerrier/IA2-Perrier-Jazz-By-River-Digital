from django.contrib import admin, messages
from allauth.account.models import EmailAddress
from ..models import CustomUser
from ..backend.auth.register.models import RegisterAuth
from ..backend.auth.forgot_password.models import ForgotPasswordAuth
from ..backend.weather_app.locationImage.models import LocationImagesModel
from ..backend.atc.events.models import Events, EventSchedule, EventScheduleItem
from ..backend.atc.events.vouchers.models import Voucher, EventVoucher
from ..backend.atc.events.food_and_drinks.models import FoodAndDrinks, EventFoodAndDrinks, FoodAndDrinksItem
from ..backend.atc.events.booking.models import Booking, BookingStatus
from ..backend.atc.events.booking.tickets.models import Tickets
from ..backend.atc.events.booking.payment.models import Payment, PaymentStatus
from ..backend.location.models import UserLocationModel
from ..backend.weather_app.chatbot.models import Message, Route
from ..backend.atc.chatbotATC.models import Message as ATCMessage
from ..backend.location.models import UserLocationModel
from ..backend.atc.models import Newsletter
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

import datetime
from django import forms
from django.contrib.auth.hashers import make_password
from import_export.admin import ImportExportModelAdmin #test
from django.urls import path
from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
import csv
import io

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
