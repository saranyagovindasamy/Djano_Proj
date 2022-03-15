#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Karthik Sivaraman
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from tb_track_app.forms.auth_forms.auth_forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required, user_passes_test
from tb_track_app.models import *
from django.http import HttpResponse
from django.http import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

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
                # import pdb; pdb.set_trace()
                if user_category == '1':
                    MD.objects.filter(name=userprofile).update(user_profile_id = user.pk)

                elif user_category == '2':
                    Trainer.objects.filter(name=userprofile).update(user_profile_id = user.pk)
                
                elif user_category == '3':
                    Trainee.objects.filter(name=userprofile).update(user_profile_id = user.pk)
                # login(request, user)
                print('success')
                data = 200
                return HttpResponse(data, content_type = 'text/plain')
        else:
            form = SignUpForm()
        return render(request, 'tb_track_app/forms/signup.html', {'form': form})
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')



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
                #return redirect('userhome')
    return render(request,'tb_track_app/accounts/login.html', {'form':form})


def change_password(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        if request.method == 'POST':
            selected_user = request.POST['username']
            new_password = request.POST['password2']
            print( selected_user, new_password)
            try:
                user = User.objects.get(username=selected_user)
                user.set_password(new_password)
                user.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            except:
                data = 409
                return HttpResponse(data, content_type = 'text/plain')      
        else:
            users = User.objects.all()
            return render(request, 'tb_track_app/accounts/change_password.html', {'users':users})
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')



def user_login_summary(request):
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        user_data = []
        user_details = []
        users = User.objects.all()
        userprofiles = UserProfile.objects.all()
        mds = MD.objects.all()
        trainers = Trainer.objects.all()
        trainees = Trainee.objects.all()

        for user in users:
            user_detail = {}
            user_id = user.id
            print('user id :', user_id)
            user_detail['user_id'] = user.id
            user_detail['username'] = user.username
            user_detail['last_login'] = user.last_login
            try:
                up_qs = userprofiles.get(user_id = user_id)
                print(up_qs)
                user_detail['user_id_field'] = up_qs.user_id_field
                user_detail['user_category'] = up_qs.user_category
                
                user_category = up_qs.user_category
        
                if user_category == '1':
                    if mds.filter(user_profile__id = user_id):
                        md = mds.filter(user_profile__id = user_id).values('name')
                        user_detail['name'] = md[0]['name']
                        
                if user_category == '2':
                    if trainers.filter(user_profile__id = user_id):
                        trainer = trainers.filter(user_profile__id = user_id).values('name')
                        user_detail['name'] = trainer[0]['name']
                        
                if user_category == '3':
                    if trainees.filter(user_profile__id = user_id):
                        trainee = trainees.filter(user_profile__id = user_id).values('name')
                        user_detail['name'] = trainee[0]['name']           
            except:
                user_detail['user_id_field'] = ""
                user_detail['user_category'] = ""
                user_detail['name'] = user.username

            user_details.append(user_detail)
        
        context ={
             'user_details':user_details,
        }
        
        return render(request, 'tb_track_app/accounts/user_login_summary.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')
