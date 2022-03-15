#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Karthik Sivaraman
# Updated Date:  19/11/2021
#####################################################################

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from tb_track_app.models import *
from tb_track_app.views.trainer_views import *
from tb_track_app.views.md_views import *
from tb_track_app.forms.trainee_forms import trainee
from django.views.generic.base import RedirectView
from django.shortcuts import render
from tb_track_project.settings import EMAIL_HOST_USER
from django.conf import settings
from django.utils.timezone import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMessage



# Create your views here.
# Landing Page view
def home(request):
    """
    :param request:
    :return: up_batches query set
    """
    print("here")
    up_batches = UpcomingBatch.objects.all().order_by('uc_batch_start_date')
    for i in up_batches:
      #print(i.uc_batch_start_date)
      if i.uc_batch_start_date.date() < datetime.now().date():
        i.delete()
    up_batches = UpcomingBatch.objects.all().order_by('uc_batch_start_date')
    context = {
            'up_batches':up_batches,
        }
    return render(request,'tb_track_app/index/home.html', context)

def switch_user_view(request):
    if request.user.is_authenticated:
        if request.user.username == 'test':
            return redirect('test-home')
        else:
            user_category = request.user.userprofile.user_category
            user_group = (Group.objects.filter(id=user_category)[0]).name
            # print(user_group)
            if user_group == "MD":
                return redirect('md-home')
            elif user_group == "Trainer":
                return redirect('trainer-home')
            elif user_group == "Trainee":
                return redirect('trainee-home')
            else:
                return render(request,'tb_track_app/index/home.html')
    return redirect('login')


# All Courses Page view
def courses(request):
    return render(request,'tb_track_app/common_template/courses.html')

# FullStack Page view
def fullstack(request):
    return render(request,'tb_track_app/common_template/fullstack_course.html')

# snowflake Page view
def snowflake(request):
    return render(request,'tb_track_app/common_template/snowflake_course.html')

# bigdata Page view
def bigdata(request):
    return render(request,'tb_track_app/common_template/bigdata_course.html')

# devops Page view
def devops(request):
    return render(request,'tb_track_app/common_template/devops_course.html')

# All Faculty Page view
def faculties(request):
    return render(request,'tb_track_app/common_template/faculties.html')

# Trainee Enroll view
def enroll(request):
    context = {}
    if request.method == "POST":
        if not TraineeEnroll.objects.filter(name=request.POST['name'], course_id = request.POST['course']).exists():
            print(request.POST['name'], request.POST['contact'],request.POST['email'], request.POST['course'],request.POST['up_batch'],request.POST['notify_future_batch'] )
            db = TraineeEnroll()
            db.name = (request.POST['name'])
            db.contact = (request.POST['contact'])# error if staut - 409
            db.email = (request.POST['email'])
            db.course_id = (request.POST['course'])
            db.language_id = (request.POST['language'])
            db.up_batch_id = (request.POST['up_batch'])
            if request.POST['notify_future_batch'] == "true":
                db.notify_future_batch = True
            else:
                db.notify_future_batch = False
            db.save()
            
            print('succuess')
            data = 200
            return HttpResponse(data, content_type='text/plain')
            
        else:
            data = 409
            return HttpResponse(data,content_type='text/plain')

    else:
        form = trainee.TraineeEnrollForm(request.POST or None)
        course_filter = Course.objects.all().distinct('name')
        context = { 
            'form':form,
            'course_filter':course_filter,
        }
    return render(request,'tb_track_app/forms/enroll_form.html',context)

def communityform(request):
    course = Course.objects.all().distinct('name')
    context ={
        'course':course,
        }
    if request.method == "POST":
        print(request.POST['firstname'],request.POST['lastname'],request.POST['email'],request.POST['phone'],request.POST['hearus'],request.POST['course'])

        db = CommunityForm()
        db.firstname = (request.POST['firstname'])
        db.lastname = (request.POST['lastname'])
        db.email = (request.POST['email'])
        db.technology_id = (request.POST['course'])
        db.hearus = (request.POST['hearus'])
        db.phone = (request.POST['phone'])
        try:
            # db.save()
            email_to = []

            email_to.append(db.email)
            subject = "Course Details"
            signature = "Regards," + '\n' + 'TamilBoomi Technologies'
            message = '\n' + '\n' + "Thanks for enquiring. Please go through the youtube link for more details." + '\n' + 'https://www.youtube.com/c/Tamilboomi' \
                                                                                                    + '\n' + '\n' + '\n' + '\n' + signature

            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, email_to)
            email_to.append(db.email)
            subject = "New Enquiry"
            signature = "Thanks"
            message = '\n' + "User " + db.firstname + " with contact number " + db.phone +" and email ID "+db.email+" has shown interest.\n\n" + signature
            #print(email_to)
            email_from = settings.EMAIL_HOST_USER
            admin_receipt = EmailMessage(subject, message, email_from, email_to,None,None,None,None,email_to,None)
            admin_receipt.send()
            #print("mailsent")
            data=200
            # return HttpResponse(data, content_type='text/plain')
            return HttpResponse(data, content_type='text/plain')
        except:
            print("Error while saving the request")
            data=500
            return HttpResponse(data, content_type='text/plain')
    else:
        return render(request,'tb_track_app/common_template/communityform.html',context)
