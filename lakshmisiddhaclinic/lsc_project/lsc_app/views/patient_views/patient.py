#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Lavanya
# Updated Date:  11/12/2021
#####################################################################
from lsc_app.forms.patient_forms.patient import *
from django.shortcuts import render, HttpResponse
from lsc_app.views.auth_views.auth_views import get_user_category

def patient_create(request):
  user_category = get_user_category(request)
  if user_category == 'MD' or user_category == "Receptionist":
    context = {}
    form = PatientCreateForm()
  if request.method == "POST":
    data = PatientBasicInfo()
    if PatientBasicInfo.objects.filter(patient_id=request.POST['patientid']).exists():
      data1 = 409
      return HttpResponse(data1, content_type='text/plain')
    data.patient_id= request.POST['patientid']
    data.dob = request.POST['dob']
    data.name = request.POST['name']
    data.mobile = request.POST['phone']
    data.emergency = request.POST['emergency']
    data.blood_group = request.POST['bloodgroup']
    data.address = request.POST['address']
    data.gender = request.POST['gender']
    data.age = request.POST['age']
    data.email = request.POST['email']
    data.aadhar= request.POST['aadhar']
    data.insurance= request.POST['insurance']
    data.emergency_contact = request.POST['emergency']
    data.save()
    data1=200
    return HttpResponse(data1, content_type='text/plain')

  context['form'] = form
  return render(request,"lsc_app/patient_template/patient_add.html",context)

def patient_add(request):
  return render(request, "lsc_app/patient_template/patient_details.html")


def patient_medical(request):
  if request.method == "POST":
    data = PatientMedicalInfo()
    try:
     info = PatientBasicInfo.objects.get(patient_id=request.POST['patientid'])
    except PatientBasicInfo.DoesNotExist:
      data1 = 409
      return HttpResponse(data1, content_type='text/plain')
    data.patient_basic_info = info
    data.allergic = request.POST['allergic']
    data.past_illness = request.POST['pastillness']
    data.past_surgery = request.POST['pastsurgery']
    data.treatment_for = request.POST['treatment']
    data.current_medication = request.POST['medication']
    data.save()
    data1 = 200
    return HttpResponse(data1, content_type='text/plain')

  return render(request, "lsc_app/patient_template/patient_medicaldetails.html")

def patient_summary(request):
    data = PatientMedicalInfo.objects.all()
    cont={'pd':data}
    return render(request,"lsc_app/patient_template/patient_summary.html",cont)
