from json.encoder import JSONEncoder
from typing import NewType
from django.shortcuts import redirect, render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, Sum, DateTimeField
from itertools import groupby
from operator import itemgetter

import datetime
import logging


@login_required(login_url='login')
def debit_transcation_create(request):
    context = {}
    if request.method == "POST":
        client_queryset = ClientProfile.objects.all()
        # print (request.POST['record_name'], request.POST['actual_name'], request.POST['contact_name'], request.POST['mobile_no'], request.POST['secondary_contact'],
            # request.POST['address'],request.POST['area_name'], request.POST['area_code'], request.POST['pending_payment'])
        date = (request.POST['debit_date'])
        client_name = (request.POST['client_name'])
        debit_amount = (request.POST['debit_amount'])
        debit_option = (request.POST['debit_option'])
        remarks = (request.POST['remarks'])
        logging.info("Debit transaction Create inititate for "+ client_name + " " + date +" "+ debit_amount+ " " + debit_option + " "+remarks)
        db = DebitTransaction()
        db.date = date
        
        db.debit_amount = debit_amount
        db.debit_option = debit_option
        db.remarks = remarks
        client_qs = client_queryset.filter(actual_name = request.POST['client_name']).first()

        db.client_id = client_qs.id
        pending_payment = client_qs.pending_payment
        new_balance = Decimal(request.POST['debit_amount']) + pending_payment
        db.open_balance = pending_payment
        db.sales_commision = 0.00
        db.close_balance = new_balance

        logging.info(" before update : "+ " pending_payment "+ str(pending_payment) + " close_balance " + str(new_balance))
        db.save()
        client_qs.pending_payment = new_balance
        client_qs.save(update_fields = ['pending_payment'])
        print('success')
        data = 200
        
        logging.info("Debit transaction Create successfully for "+ client_name + " " + date +" "+ debit_amount+ " " + debit_option + " "+remarks)
        return HttpResponse(data, content_type = 'text/plain')

    else:
        form = DebitTranscationCreateForm(request.POST or None)
        context = { 'form' : form}

    return render(request,'mss_app/debit/debit_create_form.html' , context)


@login_required(login_url='login')
def debit_transcation_summary(request):
    debittranscations = DebitTransaction.objects.all()
    context = {
        "debittranscations" : debittranscations
    }
    return render(request,'mss_app/debit/debit_transcations_summary.html' , context)



@login_required(login_url='login')
def debit_sales_bycategory(request):
    context = {}
    sales_category = DebitTransaction.objects.filter().values('date', 'debit_option').annotate(total = Sum('debit_amount'))
    total_sales = DebitTransaction.objects.filter().values('date').annotate(total_debit = Sum('debit_amount'))

    sales_grouped_values = []
    filtervalues = []
    
    # Filters sales per debit-option and reformats the dict values
    for dt, k in groupby(sorted(sales_category,key=itemgetter('date')),key=itemgetter('date')):
        for d in k:
            new = {}
            debit_option = d['debit_option']
            if debit_option == 'Auto Refill':
                debit_option='Auto_Refill'
            if debit_option == 'Manual Recharge':
                debit_option='Manual_Recharge'
            new = { 'date': d['date'], debit_option: d['total'] }
            filtervalues.append(new)
    
    # Groups values for date & amend the total_debit value
    for dt, k in groupby(filtervalues,key=itemgetter('date')):
        maindict = {'date':dt}
        for d in k:
            for q in total_sales:
                if d['date'] == q['date']:
                    d['total_debit'] = q['total_debit']
            maindict.update(d)
        
        sales_grouped_values.append(maindict)

    context = {'sales_grouped_values':sales_grouped_values}
    return render(request,'mss_app/transcation/debit_sales.html' , context)
