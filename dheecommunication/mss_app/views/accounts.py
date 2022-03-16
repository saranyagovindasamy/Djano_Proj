from statistics import mode
from turtle import home
from django.http import HttpResponseRedirect
from django.urls import path, re_path
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from mss_app.form import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

import datetime
import logging
import re

logger = logging.getLogger(__name__)


def user_login(request):

    if check_device_type(request):
        logging.info('User trying to login from mobile device')
    else:
        logging.info('User trying to login from PC/Laptop')
        userName = "not logged in"
        if not request.user.is_authenticated:
            # print(request.user.is_authenticated)
            if request.method == "POST":
                loginForm= LoginForm(request=request, data=request.POST)
                # print(loginForm.errors)
                # print(loginForm.is_valid())
                if loginForm.is_valid():
                    userName = loginForm.cleaned_data['username']
                    upass = loginForm.cleaned_data['password']
                    # print(userName, upass)
                    user = authenticate(username=userName, password=upass)
                    request.session['username'] = userName
                    # print("request.session['username']", request.session['username'])
                    logging.info("username "+ str(request.session['username']))
                    if user is not None:
                        login(request,user)
                        logging.info("login successful and will redirected to home page")
                        return HttpResponseRedirect('/home/')
                else:
                    
                    return render(request, 'mss_app/accounts/login.html')
            else:
                return render(request, 'mss_app/accounts/login.html')

def user_logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    logging.info(str(request.user)+ ' trying to log out ')
    logout(request)
    logging.info('logged out successfully at ' +str(datetime.datetime.now())+' hours!')
    return render(request, "mss_app/accounts/logged_out.html")


def check_device_type(request):

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False