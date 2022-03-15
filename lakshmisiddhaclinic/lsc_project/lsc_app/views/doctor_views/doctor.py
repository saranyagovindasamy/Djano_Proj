#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Lavanya
# Updated Date:  11/12/2021
#####################################################################
from lsc_app.forms.doctor_forms.doctor import *
from django.shortcuts import render, HttpResponse
from lsc_app.views.auth_views.auth_views import get_user_category

def doctor_create(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        form = DoctorCreateForm()
        if request.method == "POST":
            data = Doctor()
            data.doctor_id = request.POST['doctorid']
            data.name = request.POST['name']
            data.mobile = request.POST['phone']
            data.qualification = request.POST['Qualification']
            data.specilization = request.POST['Specialization']
            #if request.POST.get('male') == 'male':
             #   data.gender = 'male'
            #elif request.POST.get('male') == 'female':
             #   data.gender = 'female'
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.save()
            data1 = 200
            return HttpResponse(data1, content_type='text/plain')
        else:
            context['form']= form
            return render(request, "lsc_app/doctor_template/doctor_add_form.html", context)
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')

def doctor_home(request):
    return render(request, 'lsc_app/doctor_template/doctor_home.html')

def doctor_summary(request):
    data = Doctor.objects.all()
    context={'data':data}
    return render(request,'lsc_app/doctor_template/doctor_summary.html', context)

def doctorappoint_summary(request):
    data = Appointment.objects.filter(doctor__name=request.user)
    context = {'data':data}
    return render(request,'lsc_app/doctor_template/appointment_summary.html', context)