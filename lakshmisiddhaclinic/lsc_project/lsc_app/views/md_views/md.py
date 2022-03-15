#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  29/11/2021
# Updater     :  Lavanya
# Updated Date:  05/12/2021
#####################################################################
import datetime
import pdb


from django.contrib.auth import login, authenticate
from lsc_app.models import *
from django.shortcuts import render, HttpResponse, redirect
from lsc_app.models import *
from lsc_app.views.auth_views.auth_views import get_user_category
from lsc_app.forms.md_forms.md import *

from django.contrib.auth.models import User


def md_home(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        return render(request, "lsc_app/md_template/md_home.html")
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')



def md_create(request):
    """
       :param request:
       :return: redirects to md create page; for Post request, stores the details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        form = MdCreateForm(request.POST or None)
        if request.method == "POST":
            if not MD.objects.filter(
                    name =request.POST['name']).exists():
                db = MD()
                db.name = (request.POST['name'])
                db.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data,content_type='text/plain')
        else:
            context['form']= form
            return render(request, "lsc_app/md_template/md_add_form.html", context)
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')


def AddPatient(request):
  if request.method == "POST":
    data = PatientBasicInfo()
    data.patient_id= request.POST.get('patientid')
    data.dob = request.POST.get('dob')
    data.name = request.POST.get('name')
    data.mobile = request.POST.get('phone')
    data.emergency_contact = request.POST.get('emergency-contact')
    data.blood_group = request.POST.get('bloodgroup')
    if request.POST.get('male') == 'male':
         data.gender = 'male'
    elif request.POST.get('male') == 'female':
         data.gender = 'female'
    else:
       data.gender = 'transgender'
    data.age = request.POST.get('age')
    data.email = request.POST.get('email')
    data.aadhar=request.POST.get('aadhar')
    data.insurance=request.POST.get('insurance')
    data.save()
    return redirect('home')
    #data1="Patient Record Updated"
    #return HttpResponse(data1, content_type='text/plain')

  return render(request,"lsc_app/md_template/add_patient.html")

def Patientprofile(request):
    data = PatientMedicalInfo.objects.all()
    cont={'pd':data}
    return render(request,"lsc_app/md_template/patientprofile.html",cont)

