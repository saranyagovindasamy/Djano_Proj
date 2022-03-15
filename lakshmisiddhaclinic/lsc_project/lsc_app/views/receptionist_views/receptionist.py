#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Arun Madhu
# Updated Date:  11/12/2021
#####################################################################
from lsc_app.forms.receptionist_forms.receptionist import *
from django.shortcuts import render, HttpResponse
from lsc_app.views.auth_views.auth_views import get_user_category
from lsc_app.models import *


def receptionist_create(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        form = ReceptionistCreateForm()
        if request.method == "POST":
            data = Receptionist()
            if Receptionist.objects.filter(receptionist_id=request.POST['receptionistid']).exists():
                data1 = 409
                return HttpResponse(data1, content_type='text/plain')
            data.receptionist_id = request.POST['receptionistid']
            data.name = request.POST['name']
            data.mobile = request.POST['phone']
            data.qualification = request.POST['Qualification']
            # if request.POST.get('male') == 'male':
            #   data.gender = 'male'
            # elif request.POST.get('male') == 'female':
            #   data.gender = 'female'
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.save()
            data1 = 200
            return HttpResponse(data1, content_type='text/plain')
        else:
            context['form'] = form
            return render(request, "lsc_app/receptionist_template/receptionist_add.html", context)
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')


def receptionist_summary(request):
    data = Receptionist.objects.all()
    context = {'data': data}
    return render(request, 'lsc_app/receptionist_template/recep_summary.html', context)


def recep_home(request):
    #request.user.userprofile.user_category = '4'
    return render(request, 'lsc_app/receptionist_template/receptionist_home.html')


def recepappoint_summary(request):
    data = Bookappointment.objects.all()
    context = {'data': data}
    return render(request, 'lsc_app/common_template/appointment_summary.html', context)


def appoint_update(request):
    if request.method == "POST":
        # data = Bookappointment.objects.filter(first_visit=False)
        info = Appointment()
        name = request.POST.get('name')
        data = Bookappointment.objects.get(name=name)
        try:
         info.patient = Patient.objects.get(patient_medical_info__patient_basic_info__name=name)
        except Patient.DoesNotExist:
         return HttpResponse("Patient record not found", content_type='text/plain')
        info.appointment_time = request.POST.get('dob')
        info.description = data.reason
        try:
         info.receptionist = Receptionist.objects.get(name=request.user)
        except Receptionist.DoesNotExist:
            return HttpResponse("You are not authorised to do this action", content_type='text/plain')
        docname = request.POST.get('doctors')
        info.doctor = Doctor.objects.get(name=docname)
        info.save()
        data.delete()
        #return HttpResponse("Appointment Booked", content_type='text/plain')
        return recepappoint_summary(request)
    appt = Bookappointment.objects.all()
    doc = Doctor.objects.all()
    context = {'doc': doc, 'appt': appt}
    return render(request, 'lsc_app/receptionist_template/recep_bookapptmt.html', context)

