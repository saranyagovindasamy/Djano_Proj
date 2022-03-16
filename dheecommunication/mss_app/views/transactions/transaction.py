from http import client
from json.encoder import JSONEncoder
from multiprocessing import context
from typing import NewType
from django.shortcuts import render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse
from decimal import Context, Decimal
from django.db.models import Count, Avg, Q, Sum, DateTimeField
from django.db.models.functions import Trunc
from django.contrib.auth.decorators import login_required

def transcation_per_client(request):
    clients = ClientProfile.objects.all()
    context = {
        "clients" : clients
    }
    return render(request,'mss_app/transcation/transcation_per_client.html' , context)


import json
def load_client_transcation_by_id_ajax(request):
    client_id = request.GET['client_id']
    transaction_list = []
    debit_details = DebitTransaction.objects.filter(client_id = client_id).values('client','date','debit_amount','debit_option','open_balance','close_balance','remarks','collected_on')
    credit_details = CreditTransaction.objects.filter(client_id = client_id).values('client','date','credit_amount','credit_option','open_balance','close_balance','remarks')

    for debit in debit_details:
        transaction = {}
        transaction['type'] = 'Debit'
        transaction['client'] = debit['client']
        transaction['date'] = str(debit['date'])
        transaction['debit_amount'] = str(debit['debit_amount'])
        transaction['debit_option'] = debit['debit_option']
        transaction['open_balance'] = str(debit['open_balance'])
        transaction['close_balance'] = str(debit['close_balance'])
        transaction['collected_on'] = debit['collected_on']
        transaction_list.append(transaction)

    for credit in credit_details:
        transaction = {}
        transaction['type'] = 'Credit'
        transaction['client'] = credit['client']
        transaction['date'] = str(credit['date'])
        transaction['credit_amount'] = str(credit['credit_amount'])
        transaction['credit_option'] = credit['credit_option']
        transaction['open_balance'] = str(credit['open_balance'])
        transaction['close_balance'] = str(credit['close_balance'])
        transaction['collected_on'] = "-"
        transaction_list.append(transaction)

    data = json.dumps(transaction_list)
    print(data)
    return HttpResponse (data)
    # return render(request,'mss_app/transcation/transcation_per_client.html' , {"transaction_list":transaction_list})
    