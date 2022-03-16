from json.encoder import JSONEncoder
from typing import NewType
from django.shortcuts import redirect, render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required

import datetime
import logging

@login_required(login_url='login')
def auto_refill_summary(request):
    debittranscations = AutoRefillTransaction.objects.all()
    context = {
        "debittranscations" : debittranscations
    }
    return render(request,'mss_app/transcation/auto_refill_summary.html' , context)
