from cmath import log
from json.encoder import JSONEncoder
from typing import NewType
from django.shortcuts import redirect, render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse, HttpResponseRedirect
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tablib import Dataset
import csv
import logging
import pandas as pd


@login_required(login_url='login')
def client_import(request):
    template = 'mss_app/client/client_import_form.html'
    if "GET" == request.method:
        return render(request, template , {})
    elif request.method == 'POST':
        excel_file = request.FILES['excelfile']
        print(request.FILES['excelfile'])

        df = pd.read_excel(excel_file, header=None)
        print(df)
        print(type(df))

        for i in range(1,len(df)):
            # print(df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],
                # df.iloc[i,5],df.iloc[i,6],df.iloc[i,7],df.iloc[i,8])
            data_dict = {}
            data_dict['record_name'] = df.iloc[i,0]
            data_dict['actual_name']  = df.iloc[i,1]
            data_dict['contact_name'] = df.iloc[i,1]
            data_dict['mobile_no'] = df.iloc[i,2]
            data_dict['secondary_contact'] = None
            data_dict['address'] = None
            data_dict['area_name'] = df.iloc[i,3]
            data_dict['area_code'] = df.iloc[i,3]
            data_dict['pending_payment'] = 0.00
            
            try:
                form = ClientProfileCreateForm(data_dict)
                if form.is_valid():
                    print("Form is Valid")
                    form.save()
                    
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())	
            
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass
    
    return render(request, template)


@login_required(login_url='login')
def auto_refil_import(request):
    template = 'mss_app/transcation/auto_refill_import_form.html'
    if "GET" == request.method:
        return render(request, template , {})
    elif request.method == 'POST':
        excel_file = request.FILES['excelfile']
        logging.info("file name : "+ str(excel_file))
        df = pd.read_excel(excel_file, header=None)
        print(df)
        print(type(df))

        for i in range(1,len(df)):
            # print(df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],
                # df.iloc[i,5],df.iloc[i,6],df.iloc[i,7],df.iloc[i,8])
            data_dict = {}
            data_dict['fse_msisdn'] = df.iloc[i,0]
            data_dict['fse_name'] = df.iloc[i,1]
            data_dict['retailer_msisdn'] = df.iloc[i,2]

            # Get the client profile based on the retailer_msisdn. If doesnt exist then creates it
            try:
                data_dict['profile'] = ClientProfile.objects.get(mobile_no=df.iloc[i,2])
            except ClientProfile.DoesNotExist:
                logging.warning(" client doesnt exist "+ str(df.iloc[i,2]))
                obj = ClientProfile(record_name= df.iloc[i,3], actual_name=df.iloc[i,3],
                contact_name=None,mobile_no = df.iloc[i,2],secondary_contact=None, address= None,
                area_name= None, area_code = None, pending_payment=0.0)
                obj.save()
                logging.info("new client profile created "+ str(df.iloc[i,3])+ " "+ str(df.iloc[i,3])+ " "+ str(df.iloc[i,2])  )

            client = ClientProfile.objects.get(mobile_no=df.iloc[i,2])
            data_dict['profile'] = client
            print(data_dict['profile'])
            data_dict['retailer_name'] = df.iloc[i,3]
            data_dict['transaction_id'] = df.iloc[i,4]
            data_dict['auto_refill_date'] = df.iloc[i,5]
            data_dict['transferred_amount'] = df.iloc[i,6]
            data_dict['collectable_amount'] = df.iloc[i,7]
            data_dict['status'] = df.iloc[i,8]
            data_dict['collected_on'] = None
            data_dict['remarks'] = None

            try:
                form = AutoRefillTransactionForm(data_dict)
                if form.is_valid():
                    print("Form is Valid")
                    form.save()
                    logging.info("Auto Refill Transaction :"+ str(data_dict))
                    create_client_debit_sales(data_dict)
                else:
                    logging.error("Error occured while saving the auto refill of transaction_id " + str(df.iloc[i,4]))
                    logging.error(form.errors.as_json())
                    # logging.getLogger("error_logger").error(form.errors.as_json())	
            
            except Exception as e:
                logging.error("Exception occured")
                logging.exception(repr(e))
                # logging.getLogger("error_logger").error(repr(e))
                pass
    
    return render(request, template)


from datetime import datetime

def create_client_debit_sales(data_dict):
    date = data_dict['auto_refill_date'].split(' ')[0]
    print(date)
    debit_amount = data_dict['collectable_amount']
    debit_option = "Auto_Refill"
    client_queryset = ClientProfile.objects.all()
    client_qs = client_queryset.filter(mobile_no = data_dict['retailer_msisdn']).first()
    open_balance = client_qs.pending_payment
    close_balance = Decimal(data_dict['collectable_amount']) + client_qs.pending_payment
    sales_commision = Decimal(data_dict['collectable_amount'])*Decimal(0.01524)
    remarks = data_dict['transaction_id']
    print('db_actual_name :'+ client_qs.actual_name, 'retailer_name :'+ data_dict['retailer_name'], 'date :'+ str(date),
     'debit_amount :' + str(debit_amount), 'debit_option :'+ debit_option, 'open_balance :' + str(open_balance),
     'close_balance :'+ str(close_balance), 'sales_commision :'+ str(round(sales_commision,2)), 'remarks :',remarks)
    
    db = DebitTransaction()
    db.date = date.strip()
    db.client_id = client_qs.id
    db.debit_amount = Decimal(debit_amount)
    db.debit_option = debit_option
    db.open_balance = open_balance
    db.close_balance = close_balance
    db.sales_commision = round(sales_commision,2)
    db.remarks = str(remarks)  
    db.save()
    logging.info("Debit transaction updated for auto refill import")
    logging.info('db_actual_name :'+ client_qs.actual_name+ " "+ 'retailer_name :'+ data_dict['retailer_name']+ " "+ 'date :'+ str(date)+ " "+
     'debit_amount :' + str(debit_amount)+ " "+ 'debit_option :'+ debit_option+ " "+'open_balance :' + str(open_balance),
     'close_balance :'+ str(close_balance)+ " "+'sales_commision :'+ str(round(sales_commision,2))+ " "+ 'remarks :',remarks)
    print('success')


