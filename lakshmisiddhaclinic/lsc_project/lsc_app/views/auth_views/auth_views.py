#####################################################################
# Copyright 2021 Lakshmi Siddha clinic. All Rights Reserved.
# Owner       :  Karthik Sivaraman
# Created Date:  10/12/2021
# Updater     :  Karthik Sivaraman
# Updated Date:  11/12/2021
#####################################################################

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lsc_app.models import *
from django.http import HttpResponseRedirect, HttpResponse
from lsc_app.forms.auth_forms.auth_forms import SignUpForm, LoginForm

def get_user_category(request):
    user_group = ''
    if request.user.is_authenticated:
        user_category = request.user.userprofile.user_category
        group = (Group.objects.filter(id=user_category)[0]).name
        user_group = group
    return user_group


def signup(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user_category = (request.POST['user_category'])
                userprofile = (request.POST['userprofile_tocreate'])
                form.username = (request.POST['username'])
                form.password1 = (request.POST['password1'])
                form.password2 = (request.POST['password2'])
                form.user_category = (request.POST['user_category'])
                form.user_id_field = (request.POST['user_id_field'])
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal

                user.userprofile.user_id_field = form.cleaned_data.get('user_id_field')
                print(user.userprofile.user_id_field)
                user.userprofile.user_category = form.cleaned_data.get('user_category')
                print(user.userprofile.user_category)

                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password, )

                if user.is_authenticated:
                    print(user.pk)
                #import pdb; pdb.set_trace()
                if user_category == '1':
                    selected_user = MD.objects.get(name=userprofile)
                    selected_user.user_profile_id = user.pk
                    selected_user.save()
                elif user_category == '2':
                    selected_user = Doctor.objects.get(name=userprofile)
                    selected_user.user_profile_id = user.pk
                    selected_user.save()
                    print('success')
                elif user_category == '3':
                    selected_user = Therapist.objects.get(name=userprofile)
                    selected_user.user_profile_id = user.pk
                    selected_user.save()
                elif user_category == '4':
                    selected_user = Receptionist.objects.get(name=userprofile)
                    selected_user.user_profile_id = user.pk
                    selected_user.save()
                elif user_category == '5':
                    selected_user = Patient.objects.get(name=userprofile)
                    selected_user.user_profile_id = user.pk
                    selected_user.save()
                # login(request, user)
                print('success')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data, content_type='text/plain')
        else:
            form = SignUpForm()
        return render(request, 'lsc_app/forms/signup.html', {'form': form})
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')


def login_user(request):
    logout(request)
    username = password = ''
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('userhome'))
                # return redirect('userhome')
    return render(request, 'lsc_app/accounts/login.html', {'form': form})


def change_password(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        if request.method == 'POST':
            selected_user = request.POST['username']
            new_password = request.POST['password2']
            print(selected_user, new_password)
            try:
                user = User.objects.get(username=selected_user)
                user.set_password(new_password)
                user.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            except:
                data = 409
                return HttpResponse(data, content_type='text/plain')
        else:
            users = User.objects.all()
            return render(request, 'lsc_app/accounts/change_password.html',
                          {'users': users})
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')


def user_login_summary(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        user_data = []
        user_details = []
        users = User.objects.all()
        userprofiles = UserProfile.objects.all()
        mds = MD.objects.all()
        doctors = Doctor.objects.all()
        therapists = Therapist.objects.all()
        receptionists = Receptionist.objects.all()
        patients = Patient.objects.all()

        for user in users:
            user_detail = {}
            user_id = user.id
            user_detail['user_id'] = user.id
            user_detail['username'] = user.username
            user_detail['last_login'] = user.last_login

            up_qs = userprofiles.filter(user_id=user_id).values('user_id_field',
                                                                'user_category')
            user_detail['user_id_field'] = up_qs[0]['user_id_field']
            user_detail['user_category'] = up_qs[0]['user_category']

            user_category = up_qs[0]['user_category']

            if user_category == '1':
                if mds.filter(user_profile__id=user_id):
                    md = mds.filter(user_profile__id=user_id).values('name')
                    user_detail['name'] = md[0]['name']

            if user_category == '2':
                if doctors.filter(user_profile__id=user_id):
                    doctor = doctors.filter(user_profile__id=user_id).values(
                        'name')
                    user_detail['name'] = doctor[0]['name']

            if user_category == '3':
                if therapists.filter(user_profile__id=user_id):
                    therapist = therapists.filter(user_profile__id=user_id).values(
                        'name')
                    user_detail['name'] = therapist[0]['name']

            if user_category == '4':
                if receptionists.filter(user_profile__id=user_id):
                    receptionist = receptionists.filter(user_profile__id=user_id).values(
                        'name')
                    user_detail['name'] = receptionist[0]['name']

            if user_category == '5':
                if patients.filter(user_profile__id=user_id):
                    patient = patients.filter(user_profile__id=user_id).values(
                        'name')
                    user_detail['name'] = patient[0]['name']
            user_details.append(user_detail)

        context = {
            'user_details': user_details,
        }

        return render(request, 'lsc_app/accounts/user_login_summary.html',
                      context)
    else:
        return render(request, 'lsc_app/accounts/unauthorized.html')