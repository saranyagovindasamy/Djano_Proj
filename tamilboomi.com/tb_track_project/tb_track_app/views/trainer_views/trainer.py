#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################

from django.shortcuts import render
from tb_track_app.models import *
from django.http import HttpResponse
from tb_track_app.forms.trainer_forms import trainer
from tb_track_app.views.auth_views.auth_views import get_user_category


def trainer_create(request):
    """
       :param request:
       :return: redirects to Trainer create page; for POST request, stores the Trainer Details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context = {}
        if request.method == "POST":
            if not Trainer.objects.filter( language_id = request.POST['language'] , name = request.POST['name']).exists():
                print(request.POST['name'], request.POST['contact'],request.POST['email'], request.POST['course'],request.POST['language'] )
                db = Trainer()
                db.name = (request.POST['name'])
                db.contact = (request.POST['contact'])
                db.email = (request.POST['email'])
                db.language_id = (request.POST['language'])
                db.course_id = (request.POST['course'])
                db.fixed_monthly_salary = (request.POST['fixed_monthly_salary'])
                db.salary_percent = (request.POST['salary_percent'])
                db.variable_salary_percent = (request.POST['variable_salary_percent'])
                db.save()
                print('success')
                data = 200
                return HttpResponse(data, content_type = 'text/plain')
            else:
                print(request.POST['name'], request.POST['contact'],request.POST['email'], request.POST['course'],request.POST['language'] )
                data = 409
                return HttpResponse(data, content_type = 'text/plain')
        else:
            form = trainer.TrainerCreateForm(request.POST or None)
            course_filter = Course.objects.all().distinct('name')
            context = { 
                'form':form,
                'course_filter':course_filter,
            }
        return render(request,'tb_track_app/trainer_template/trainer_add_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainer_details(request):
    """
       :param request:
       :return: redirects to Trainer summary page
    """  
    user_category = get_user_category(request)
    if user_category == 'MD':
        trainers = Trainer.objects.all()
        context = {
            "trainers": trainers,
                }
        return render(request, 'tb_track_app/trainer_template/trainer_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')



def trainer_home(request):
    """
       :param request:
       :return: redirects to Trainr's Home page with releavant details
    """   
    user_category = get_user_category(request)
    if user_category == 'Trainer':
        # Fetching All Students under Staff
        user = request.user
        trainer = Trainer.objects.filter(user_profile_id = user.id).values('name','email','id','user_profile__username','user_profile__last_login')
        batchs = Batch.objects.filter(trainer = trainer[0]['id'])
        trainees_count = 0
        for batch in batchs:
            count = Trainee.objects.filter(batch_id = batch.id).count()
            if count != 0:
                trainees_count += count
    
        subject_list = []
        attendance_list = []
        trainee_list = []
        trainee_list_attendance_present = []
        trainee_list_attendance_absent = []
        
        context ={

            "trainees_count": trainees_count,
            "attendance_count": 2,
            "leave_count": 2,
            "subject_count": 2,
            "subject_list": subject_list,
            "attendance_list": attendance_list,
            "trainee_list": trainee_list,
            "attendance_present_list": trainee_list_attendance_present,
            "attendance_absent_list": trainee_list_attendance_absent,
            "trainer":trainer,
            "user" : user
        }

        return render(request, "tb_track_app/trainer_template/trainer_home.html", context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainer_attendance(request):
    """
       :param request:
       :return: redirects to Trainees Attendance page with releavant details; for Post request stores the attendance details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'Trainer':
        course_details = []
        if request.method == 'POST':
            # import pdb; pdb.set_trace()
            trainees_status = eval(request.POST['trainees_status'])
            trainees_details = eval(request.POST['trainees_details'])
            for trainee in trainees_details:
                id = trainee['trainee_id']
                db = Attendance()
                db.trainee_id = id
                db.language = trainee['language']

                if id in trainees_status:
                    print(trainee['trainee_id'] + 'is present for ' + trainee['language'] )
                    db.status = 1
                    pass
                else:
                    print(trainee['trainee_id'] + 'is absent for ' + trainee['language'])
                    db.status = 0
                db.save()
                data = 200
                print('success')

            return HttpResponse(data, content_type='text/plain')
        else:
            user = request.user
            trainer = Trainer.objects.filter(user_profile_id = user.id).values('id')
            batch_qs = Batch.objects.all()
            batches = batch_qs.filter(trainer_id=trainer[0]['id']).values('id','name','course_id','course__name').distinct('course_id')
            for batch in batches:
                course ={}
                print(batch)
                course['id'] = batch['course_id']
                course['name'] = batch['course__name']
                course_details.append(course)

            return render(request, 'tb_track_app/trainer_template/trainer_attendance.html',
                        {"course_details": course_details}
                        )
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainer_attendance_summary(request):
    """
       :param request:
       :return: redirects to Trainee's Attendance summary page with releavant details
    """   
    user_category = get_user_category(request)
    if user_category == 'Trainer' or user_category == 'MD':
        trainees_attendance = Attendance.objects.all()

        return render(request, 'tb_track_app/trainer_template/trainer_attendance_summary.html', { "trainees_attendance":trainees_attendance })
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainer_payment_add(request):
    """
       :param request:
       :return: redirects to Trainer's payment add page; for Post request, stored the payment details and returns a HttpResnsposne accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        if request.method == "POST":
            batch = (request.POST['batch_id'])
            trainer_id= (request.POST['trainer_id'])
            selected_trainer = Trainer.objects.get(id = trainer_id)
            contact = selected_trainer.contact
            salary_percent = selected_trainer.salary_percent
            contact = selected_trainer.contact
            course__id = selected_trainer.course
            trainee_count = Trainee.objects.filter(batch_id = batch).count()
            course_qs = CourseFees.objects.filter(course_id = course__id).values('id','course_fee','created_at')
            course_fee = course_qs[0]['course_fee']
            amount_to_be_paid = ((trainee_count*course_fee) * (salary_percent/100))
            tp_qs = TrainerPayment.objects.all()
            course_id = (request.POST['course_id'])
            tp_qs = TrainerPayment.objects.all()
            try:
                tp = tp_qs.filter(name_id= trainer_id, batch_id=batch).latest('created_at')

                if amount_to_be_paid > tp.amount_to_be_paid:
                    amount_to_be_paid = amount_to_be_paid
                else:
                    amount_to_be_paid = tp.amount_to_be_paid

                total_amount_paid = tp.total_amount_paid + int(request.POST['amount_paying'])
                if total_amount_paid == amount_to_be_paid:
                    balance_salary =0
                else:
                    balance_salary = amount_to_be_paid - total_amount_paid
            except:
                total_amount_paid = 0 + int(request.POST['amount_paying'])
                balance_salary = amount_to_be_paid - total_amount_paid

            db = TrainerPayment()
            db.name_id = trainer_id
            db.contact = contact
            db.course_id = course_id
            db.batch_id = batch
            db.amount_paid = (request.POST['amount_paying'])
            db.total_amount_paid =total_amount_paid
            db.balance_salary = balance_salary
            db.date = (request.POST['payment_date'])
            db.remarks = (request.POST['remarks'])
            db.payment_reason = (request.POST['payment_reason'])
            db.amount_to_be_paid = amount_to_be_paid
            db.save()
            print('success')
            data = 200
            return HttpResponse(data, content_type = 'text/plain')
        
        else:
            form = trainer.TrainerPaymentAddForm(request.POST or None)
            trainer_filter = Trainer.objects.all().distinct('name')
            context = { 
                'form':form,
                'trainer_filter':trainer_filter,
            }
        return render(request, "tb_track_app/trainer_template/trainer_payment_add_form.html", context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def trainer_payment_details(request):
    """
       :param request:
       :return: redirects to Trainer's payment summary page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        trainers = TrainerPayment.objects.all()
        context = {
            "trainers": trainers,        
        }
        return render(request, 'tb_track_app/trainer_template/trainer_payment_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')

