from genericpath import exists
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
def mcash_transcation_create(request):
    mcash_transcations = MCashTranscations.objects.all()
    context = {}

    if request.method == "POST":
        db = MCashTranscations()

        date = request.POST['mcash_date']
        mcash_amount = request.POST['mcash_amount']
        sales_commision = request.POST['sales_commision']
        retailer_commision = request.POST['retailer_commision']
        distributor_commision = request.POST['distributor_commision']
        db.date = date
        db.mcash_amount = mcash_amount
        db.sales_commision = sales_commision
        db.retailer_commision = retailer_commision 
        db.distributor_commision = distributor_commision
        try:
            qs = MCashTranscations.objects.latest('id')
            qs_closing_balance = qs.closing_balance
        except MCashTranscations.DoesNotExist:
            qs_closing_balance = "0.00"
        # print(qs.opening_balance, qs.closing_balance)
        opening_balance = qs_closing_balance
        closing_balance = Decimal(qs_closing_balance) + Decimal(distributor_commision)
        db.opening_balance = opening_balance
        db.closing_balance = closing_balance
        # print(qs.opening_balance + Decimal(request.POST['distributor_commision']))
        db.save()
        logging.info("mcash transaction created "+ " "+ str(date)+ " "+ str(mcash_amount)+ " "+str(sales_commision)
        + " "+str(distributor_commision)+ " "+ 'opening_balance :' + str(opening_balance)+ " "+ 'closing_balance:'+ str(closing_balance))
        print('success')
        data = 200
        return HttpResponse(data, content_type = 'text/plain')

    else:
        form = MCashTranscationCreateForm(request.POST or None)
        context = { 'form' : form, 'mcash_transcations': mcash_transcations}

    return render(request,'mss_app/transcation/mcash.html' , context)


@login_required(login_url='login')
def load_mcash_ajax(request):
    data = []
    qs = MCashTranscations.objects.latest('id')
    # print(qs.id, qs.date,qs.mcash_amount, qs.sales_commision)
    data.append(qs.id)
    data.append(',')
    data.append(qs.date)
    data.append(',')
    data.append(qs.mcash_amount)
    data.append(',')
    data.append(qs.sales_commision)
    data.append(',')
    data.append(qs.retailer_commision)
    data.append(',')
    data.append(qs.distributor_commision)
    data.append(',')
    data.append(qs.opening_balance)
    data.append(',')
    data.append(qs.closing_balance)
    logging.info("mcash transaction appended "+ " "+ str(data))

    return HttpResponse (data)