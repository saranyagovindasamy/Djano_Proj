#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################
from django.contrib.auth import BACKEND_SESSION_KEY
from django.shortcuts import render
from tb_track_app.models import *
from tb_track_app.forms.trainee_forms import trainee
from django.http import HttpResponse
from tb_track_app.views.auth_views.auth_views import get_user_category


def trainee_home(request):
    """
       :param request:
       :return: redirects to Trainee Home
    """
        # Fetching All Students under Staff
    context ={
    }

    return render(request, "tb_track_app/trainee_template/trainee_home.html", context)


def trainee_create(request):
    """
       :param request:
       :return: redirects to New Traine create page; for POST request, stores the new Trainee Details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        if request.method == "POST":

            if not Trainee.objects.filter( course_id = request.POST['course'] , name = request.POST['name']).exists():

                print(request.POST['name'], request.POST['contact'],request.POST['email'], request.POST['course'],request.POST['batch'] )
                db = Trainee()
                db.name = (request.POST['name'])
                db.contact = (request.POST['contact'])
                db.email = (request.POST['email'])
                db.course_id = (request.POST['course'])
                db.batch_id = (request.POST['batch'])
                db.save()

                print('success')
                data = 200
                return HttpResponse(data, content_type = 'text/plain')
            else:
                data = 409
                return HttpResponse(data, content_type = 'text/plain')
        else:
            form = trainee.TraineeCreateForm(request.POST or None)
            course_filter = Course.objects.all().distinct('name')
            context = { 
                'form':form,
                'course_filter':course_filter,
            }
        return render(request, "tb_track_app/trainee_template/trainee_add_form.html", context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')

def trainee_details(request):
    """
       :param request:
       :return: redirects to Traine summary page with contaxt of all Trainee's details for MD user;
        For trainer's with only releavant trainee' details
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        trainees = Trainee.objects.all()

        context = {
            "trainees": trainees,
        
        }
        return render(request, 'tb_track_app/trainee_template/trainee_details.html', context)

    elif user_category == 'Trainer':
        trainee_details = []
        user = request.user
        trainer = Trainer.objects.filter(user_profile_id = user.id).values('id')
        print(trainer)
        batch_qs = Batch.objects.all()
        batches = batch_qs.filter(trainer_id=trainer[0]['id']).values('id','name','course_id','course__name')
        print(batches)
        for batch in batches:
            print('batch id',batch['id'])
            trainee_qs = Trainee.objects.filter(batch_id = batch['id'])
            for trainee in trainee_qs:
                print(trainee)
                trainee_details.append(trainee)

        context = {
            "trainees": trainee_details
        }
        return render(request, 'tb_track_app/trainee_template/trainee_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainee_fees_add(request):
    """
       :param request:
       :return: redirects to Traine fee add page; for POST request, stores the payment Details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        if request.method == "POST":
            print(request.POST['course_id'], request.POST['batch_id'], request.POST['trainee_name'], request.POST['payment_date'],request.POST['amount_paying'],
            request.POST['remarks'])
            course_fee_qs = CourseFees.objects.get(course_id = request.POST['course_id'])
            course_fee = course_fee_qs.course_fee
            trainee_name = (request.POST['trainee_name'])
            selected_trainee = Trainee.objects.get(name = trainee_name)
            trainee_id = selected_trainee.id
            contact = selected_trainee.contact
            course = selected_trainee.course
            batch = selected_trainee.batch
            batch_id = (request.POST['batch_id'])
            ts_qs = TraineeFees.objects.all()
            try:
                ts_fees = ts_qs.filter(name_id=trainee_id, batch_id= batch_id).latest('created_at')
                total_fees_paid = ts_fees.total_fees_paid + int(request.POST['amount_paying'])
                balance_fee = course_fee - total_fees_paid
            except:
                total_fees_paid = 0 + int(request.POST['amount_paying'])
                balance_fee = course_fee - total_fees_paid

            db = TraineeFees()
            db.name_id = trainee_id
            db.contact = contact
            db.course = course
            db.batch_id = (request.POST['batch_id'])
            db.amount_paid = (request.POST['amount_paying'])
            db.total_fees_paid =total_fees_paid
            db.balance_fee = balance_fee
            db.date = (request.POST['payment_date'])
            db.remarks = (request.POST['remarks'])
            db.save()
            print('success')
            data = 200
            return HttpResponse(data, content_type = 'text/plain')
        
        else:
            form = trainee.TraineeFeesAddForm(request.POST or None)
            course_filter = Course.objects.all().distinct('name')
            context = { 
                'form':form,
                'course_filter':course_filter,
            }
        return render(request, "tb_track_app/trainee_template/trainee_fee_add_form.html", context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainee_fees_details(request):
    """
       :param request:
       :return: redirects to Traine fee summary page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        trainees = TraineeFees.objects.all()

        context = {
            "trainees": trainees,
        
        }
        return render(request, 'tb_track_app/trainee_template/trainee_fees_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')