from json.encoder import JSONEncoder
from typing import NewType
from django.shortcuts import redirect, render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse, HttpResponseRedirect
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import openpyxl

import logging

logger = logging.getLogger(__name__)

@login_required(login_url='login')
def client_profile_create(request):
    context = {}
    if request.method == "POST":
        if not ClientProfile.objects.filter(mobile_no = request.POST['mobile_no']).exists():
            print (request.POST['record_name'], request.POST['actual_name'], request.POST['contact_name'], request.POST['mobile_no'], request.POST['secondary_contact'],
             request.POST['address'],request.POST['area_name'], request.POST['area_code'], request.POST['pending_payment'])
            db = ClientProfile()
            db.record_name = (request.POST['record_name'])
            db.actual_name = (request.POST['actual_name'])
            db.contact_name = (request.POST['contact_name'])
            db.mobile_no = (request.POST['mobile_no'])
            db.secondary_contact = (request.POST['secondary_contact'])
            db.address = (request.POST['address'])
            db.area_name = (request.POST['area_name'])
            db.area_code = (request.POST['area_code'])
            db.pending_payment = (request.POST['pending_payment'])
            db.save()
        
            print('success')
            data = 200
            logging.info(str(request.POST['record_name']) + " " + str(request.POST['actual_name']) 
            + " " + str(request.POST['contact_name']) + " " + str(request.POST['mobile_no']) + " " 
            + str(request.POST['secondary_contact']) + " " + str(request.POST['address'])+ " " +
            str(request.POST['area_name']) + " " + str(request.POST['area_code']) + " " +
            str(request.POST['pending_payment'])+" " + "client profile created successfully")
            return HttpResponse(data, content_type = 'text/plain')
        else:
            data = 409
            logging.warning(str(request.POST['record_name']) + " " + str(request.POST['actual_name']) 
            + " " + str(request.POST['contact_name']) + " " + str(request.POST['mobile_no']) + " " 
            + "client profile exist already")
            return HttpResponse(data, content_type = 'text/plain')
    else:
        form = ClientProfileCreateForm(request.POST or None)
        context = { 'form' : form}

    return render(request,'mss_app/client/client_profile_create_form.html' , context)


@login_required(login_url='login')
def client_edit(request, client_id):
    logging.info("User tring to edit the profile of client-id = "+ str(client_id))
    client = ClientProfile.objects.get(id=client_id)
    logging.info("Selected client current details --> "+ str(client.record_name) + " " +
    str(client.actual_name)+ " " + str(client.contact_name)+ " "+str(client.mobile_no)
    + " "+str(client.secondary_contact)+ " "+str(client.address)+ " "+ str(client.area_name)+ " "+
    str(client.area_code)+ " "+ str(client.pending_payment))
    context = {
        'client':client,
        'id':client_id
    }
    return render(request,'mss_app/client/client_profile_edit_form.html' , context)


@login_required(login_url='login')
def client_edit_save(request):
    if request.method == "POST":
        client_id = (request.POST['client_id'])
        record_name = (request.POST['record_name'])
        actual_name = (request.POST['actual_name'])
        contact_name = (request.POST['contact_name'])
        mobile_no = (request.POST['mobile_no'])
        secondary_contact = (request.POST['secondary_contact'])
        address = (request.POST['address'])
        area_name = (request.POST['area_name'])
        area_code = (request.POST['area_code'])
        pending_payment = (request.POST['pending_payment'])

        print(client_id, record_name, actual_name, contact_name,mobile_no,secondary_contact,address,area_name,area_code,pending_payment)
        
        try:

            client_model = ClientProfile.objects.get(id = client_id)
            client_model.record_name = record_name
            client_model.actual_name = actual_name
            client_model.contact_name = contact_name
            client_model.mobile_no = mobile_no
            client_model.secondary_contact = secondary_contact
            client_model.address = address
            client_model.area_name = area_name
            client_model.area_code = area_code
            client_model.pending_payment = pending_payment
            client_model.save()

            messages.success(request, "Client Details updated Successfully.")
            print('success')
            data = 200

            logging.info("client details udpated " + client_id+ " " + record_name+ " " + actual_name+ " " + 
            contact_name+ " " +mobile_no+ " " +secondary_contact+ " " +address+ " " 
            +area_name+ " " +area_code+ " " +pending_payment)
            return HttpResponse(data, content_type = 'text/plain')
        
        except:
            messages.error(request, "Client Details failed to update.")
            logging.warning( client_id+ " " + record_name+ " " + actual_name+ " " + " failed to update.")
            data = 409
            return HttpResponse(data, content_type = 'text/plain')


@login_required(login_url='login')
def client_details(request):
    clients = ClientProfile.objects.all()
    context = {
        "clients" : clients
    }
    return render(request,'mss_app/client/client_profile_summary.html' , context)



@login_required(login_url='login')
def load_client_ajax(request):
    data = []
    qs = ClientProfile.objects.all()
    client_name = request.GET['client_name']
    print('selected client', client_name)
    logging.info( 'selected client '+ client_name)
    selected_client = qs.filter(actual_name = client_name).first()
    print('client query', selected_client)
    record_name = selected_client.record_name
    mobile_no = selected_client.mobile_no
    contact_name = selected_client.contact_name
    area_name = selected_client.area_name
    pending_payment = selected_client.pending_payment

    print(record_name, contact_name,area_name, pending_payment)
    logging.info('load_client_ajax :'+ " " +record_name + " " + contact_name + " " + mobile_no + " " +area_name + " " +  str(pending_payment))
    data.append(record_name)
    data.append(',')
    data.append(contact_name)
    data.append(',')
    data.append(mobile_no)
    data.append(',')
    data.append(area_name)
    data.append(',')
    data.append(pending_payment)
    # data = { record_name ,contact_name, mobile_no, area_name}
    return HttpResponse (data)


def load_client_by_id_ajax(request):
    data = []
    client_id = request.GET['client_id']
    logging.info( 'selected client id '+ str(client_id))
    qs = ClientProfile.objects.all()
    selected_client = qs.filter(id = client_id).first()
    logging.info( 'selected client '+ str(selected_client))
    print('client query', selected_client)
    record_name = selected_client.record_name
    mobile_no = selected_client.mobile_no
    contact_name = selected_client.contact_name
    area_name = selected_client.area_name
    pending_payment = selected_client.pending_payment

    print(record_name, contact_name,area_name, pending_payment)
    logging.info('load_client_by_id_ajax :'+ " " +record_name + " " + contact_name +  " " + mobile_no  + " " + area_name + " " +  str(pending_payment))
    data.append(record_name)
    data.append(',')
    data.append(contact_name)
    data.append(',')
    data.append(mobile_no)
    data.append(',')
    data.append(area_name)
    data.append(',')
    data.append(pending_payment)
    # data = { record_name ,contact_name, mobile_no, area_name}
    return HttpResponse (data)


