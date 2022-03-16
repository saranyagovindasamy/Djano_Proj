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
def credit_transaction_create(request):
    context = {}
    if request.method == "POST":
        client_queryset = ClientProfile.objects.all()
            # print (request.POST['record_name'], request.POST['actual_name'], request.POST['contact_name'], request.POST['mobile_no'], request.POST['secondary_contact'],
                # request.POST['address'],request.POST['area_name'], request.POST['area_code'], request.POST['pending_payment'])
        db = CreditTransaction()
        date = (request.POST['credit_date'])
        credit_amount = (request.POST['credit_amount'])
        client_name = (request.POST['client_name'])
        credit_option = (request.POST['credit_option'])
        remarks = (request.POST['remarks'])

        db.date = date
        db.credit_amount = credit_amount 
        db.credit_option =  credit_option 
        db.remarks = remarks 
        logging.info("Credit transaction Create inititate for "+ client_name + " " + date +" "+ credit_amount+ " " + credit_option + " "+remarks)
        client_qs = client_queryset.get(actual_name = request.POST['client_name'])
        print(client_qs)
        print(client_qs.id)
        db.client_id = client_qs.id
        pending_payment = client_qs.pending_payment
        new_balance = pending_payment -  Decimal(request.POST['credit_amount'])
        db.open_balance = pending_payment
        db.sales_commision = 0.00
        db.close_balance = new_balance
        print('close_balance', new_balance)
        logging.info(" before update : "+ " pending_payment "+ str(pending_payment) + " close_balance " + str(new_balance))
        db.save()
        client_qs.pending_payment = new_balance
        client_qs.save(update_fields = ['pending_payment'])
        print('success')
        data = 200
        logging.info("Credit transaction Create successfully for "+ client_name + " " + date +" "+ credit_amount+ " " + credit_option + " "+remarks)
        return HttpResponse(data, content_type = 'text/plain')

    else:
        form = CreditTranscationCreateForm(request.POST or None)
        context = { 'form' : form}

    return render(request,'mss_app/credit/credit_create_form.html' , context)


@login_required(login_url='login')
def credit_transaction_summary(request):
    credittransactions = CreditTransaction.objects.all()
    context = {
        "credittransactions" : credittransactions
    }
    return render(request,'mss_app/credit/credit_transcations_summary.html' , context)


@login_required(login_url='login')
def credit_sales_bycategory(request):
    context = {}
    sales_category = CreditTransaction.objects.filter().values('date', 'credit_option').annotate(total = Sum('credit_amount'))
    total_credit_sales = CreditTransaction.objects.filter().values('date').annotate(total_credit = Sum('credit_amount'))
    
    sales_grouped_values = []
    filtervalues = []
    
    # for sales in sales_category:
    #     print('credit', sales)
    
    # for total in total_credit_sales:
    #     print('total',total)

    # Filters sales per debit-option and reformats the dict values
    for dt, k in groupby(sorted(sales_category,key=itemgetter('date')),key=itemgetter('date')):
        for d in k:
            new = {}
            credit_option = d['credit_option']
            if credit_option == 'G-PAY':
                credit_option = 'Gpay'
            new = { 'date': d['date'], credit_option: d['total'] }
            filtervalues.append(new)
    
    # Groups values for date & amend the total_debit value
    for dt, k in groupby(filtervalues,key=itemgetter('date')):
        maindict = {'date':dt}
        for d in k:
            for q in total_credit_sales:
                # print(q)
                if d['date'] == q['date']:
                    d['total_credit'] = q['total_credit']
            maindict.update(d)
        
        sales_grouped_values.append(maindict)

    # print(sales_grouped_values)
    context = {'sales_grouped_values':sales_grouped_values}
    return render(request,'mss_app/transcation/credit_sales.html' , context)
