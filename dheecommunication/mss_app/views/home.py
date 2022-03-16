from json.encoder import JSONEncoder
from typing import NewType
from django.shortcuts import redirect, render
from mss_app.models import *
from mss_app.form import *
from django.http import HttpResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from mss_app.tasks import go_to_sleep
from mss_app.views.accounts import user_login
import datetime
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    # print("request.session['username']",request.session['username'])
    if 'username' in request.session:
        username = request.session['username']
        logging.info(username+ ' logged in '+str(datetime.datetime.now())+' hours!')
        logging.info(request.headers['User-Agent'])
        # print(request.headers['User-Agent'])
        # print(username)
        return render(request,'mss_app/home.html')
    else:
        logging.warning("A user tried to access Home page without login. Will be redirected to Login Page")
        logging.info(request.headers['User-Agent'])
        return redirect(user_login)




def index(request):
    task = go_to_sleep.delay(0.05)
    
    return render(request, 'mss_app/progress.html', {'task_id' : task.task_id})