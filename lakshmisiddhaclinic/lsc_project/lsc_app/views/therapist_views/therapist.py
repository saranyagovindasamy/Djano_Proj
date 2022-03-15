#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Arun Madhu
# Updated Date:  11/12/2021
#####################################################################
from lsc_app.forms.therapist_forms.therapist import *
from django.shortcuts import render, HttpResponse
from lsc_app.views.auth_views.auth_views import get_user_category


def therapist_create(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        form = TherapistCreateForm()
        if request.method == "POST":
            data = Therapist()
            data.therapist_id = request.POST['therapistid']
            data.name = request.POST['name']
            data.mobile = request.POST['phone']
            data.qualification = request.POST['Qualification']
            data.specilization = request.POST['Specialization']
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
            return render(request, "lsc_app/therapist_template/therapist_add.html", context)
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')


def therapist_summary(request):
    data = Therapist.objects.all()
    context = {'data': data}
    return render(request, 'lsc_app/therapist_template/therapist_summary.html', context)