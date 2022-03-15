#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Arun Madhu
# Updated Date:  11/12/2021
#####################################################################

from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from lsc_app.forms.md_forms import md
from django.http import HttpResponse
from lsc_app.models import *
from datetime import datetime
import json


def load_selected_category_users_ajax(request):
    """
       :param request:
       :return: returns a a HttpResponse of users list for the selected user category
    """
    user_category = request.GET['user_category']

    if user_category == 'MD':
        users = MD.objects.all()
    
    if user_category == 'Doctor':
        users = Doctor.objects.all()

    if user_category == 'Therapist':
        users = Therapist.objects.all()

    if user_category == 'Receptionist':
        users = Receptionist.objects.all()

    #print(users)
    cd = set(users.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)  


def suggest_username_ajax(request):
    """
       :param request:
       :return: returns a a HttpResponse of valid new username for the selcted user profile
    """
    user_name = request.GET['user_name']
    print(user_name)
    users = User.objects.filter(username=user_name)
    print(users)
    user_profile = UserProfile.objects.all()
    last_user = user_profile.latest('user_id_field')
    print (last_user)
    new_user_id_field = int(last_user.user_id_field) + 1
    print(new_user_id_field)
    if not User.objects.filter(username=user_name).exists():
        data = new_user_id_field
        return HttpResponse(data, content_type='text/plain')
    else:
        data = 409
        return HttpResponse(data,content_type='text/plain')


from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt,csrf_protect

@csrf_exempt
def load_blog_images_ajax(request):
    upload = request.FILES['image']
    print(upload)
    fss = FileSystemStorage()
    # django-summernote/" + datetime.datetime.now().strftime("%Y/%m")
    file = fss.save(upload.name, upload)
    print(file)
    file_url = fss.url(file)
    print (file_url)
    return HttpResponse(file_url)