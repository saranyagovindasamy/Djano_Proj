#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  15/11/2021
#####################################################################
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from tb_track_app.forms.md_forms import md
from django.http import HttpResponse
from tb_track_app.models import *
from datetime import datetime
import json
from tb_track_app.models import *


def load_selected_category_users_ajax(request):
    """
       :param request:
       :return: returns a a HttpResponse of users list for the selected user category
    """
    user_category = request.GET['user_category']

    if user_category == 'MD':
        users = MD.objects.all()
    elif user_category == 'Trainer':
        users = Trainer.objects.all()
    elif user_category == 'Trainee':
        users = Trainee.objects.all()
   
    print(users)
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
    new_user_id_field = int(last_user.user_id_field) + 1
    # print(new_user_id_field)
    if not User.objects.filter(username=user_name).exists():
        data = new_user_id_field
        return HttpResponse(data, content_type='text/plain')
    else:
        data = 409
        return HttpResponse(data,content_type='text/plain')


def load_courses_md_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of Course details for the selected course
    """
    language =  request.GET['language']
    print(language)
    courses = Course.objects.filter(language__name=language)
    print(courses)
    cd = set(courses.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_trainer_md_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of Trainer details for the selected course & programming language
    """
    language =  request.GET['language']
    course = request.GET['course']
    # print(language, course)
    trainer = Trainer.objects.filter(language__name=language).filter(course__name = course)
    # print(trainer)
    cd = set(trainer.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_courses_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse courses based on the selected programming language
    """    
    lang_name = request.GET['lang_name']
    course_details = Course.objects.filter(language__name=lang_name)
    cd = set(course_details.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_trainer_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of selected course Trainer's details
    """
    #import pdb;pdb.set_trace()
    course_name = request.GET['course_name']
    #batch_details = Trainer.objects.filter(course_id__name=trainer_name)
    trainer_details = Trainer.objects.filter(course_id__name=course_name)
    td = set(trainer_details.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(td))
    return HttpResponse(result)


def load_languages_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of selected course programming language details
    """        #import pdb;pdb.set_trace()
    lang_list = []
    course_name = request.GET['course']
    lang_qs = ProgrammingLanguage.objects.all()
    qs =  Course.objects.all()
    # print(course_name)
    #batch_details = Trainer.objects.filter(course_id__name=trainer_name)
    language_details = qs.filter(name=course_name)
    for lang in language_details:
        # print(lang)
        lang_name = lang_qs.get(id = lang.language_id)
        lang_list.append(lang_name.name + '-' + str(lang_name.id))
        print(lang_name.name)
    # print(language_details)
    td = set(lang_list)
    result = '''{}'''.format(list(td))
    return HttpResponse(result)


def load_batch_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of selected course batch details
    """        #import pdb;pdb.set_trace()
    batch_list = []
    course_name = request.GET['course']
    course_qs =  Course.objects.all()
    # print(course_name)
    #batch_details = Trainer.objects.filter(course_id__name=trainer_name)
    course_details = course_qs.filter(name=course_name)
    for course in course_details:
        # print(course)
        # print(course.id)
        batches = Batch.objects.filter(course_id = course.id).values('id','name','course_id')
        # print(batches)
        for batch in batches:
            batch_list.append(str(batch['name']) + '#' + str(batch['id']))
            # print(batch['start_date'])
    # print(language_details)
    td = set(batch_list)
    result = '''{}'''.format(list(td))
    return HttpResponse(result)


def load_language_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of selected course's Programming Language details
    """
    course_name = request.GET['course_name']
    course_details = Course.objects.filter(name=course_name)
    ld = set(course_details.values_list('language__name', flat=True).distinct())
    result = '''{}'''.format(list(ld))
    return HttpResponse(result)


def load_trainerbatch_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of trainer's selected course batch details
    """
    batch_list = []
    course_name = request.GET['course_name']
    course_details = Batch.objects.filter(course__name=course_name,trainer__name=request.user).values('start_date','id')
    for batch in course_details:
     batch_list.append(str(batch['start_date']) + '#' + str(batch['id']))
    ted = set(batch_list)
    result = '''{}'''.format(list(ted))
    # print(result)
    return HttpResponse((result))


from datetime import datetime
def load_enroll_batch_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of selected course upcoming batch details
    """
        #import pdb;pdb.set_trace()
    batch_list = []
    course_name = request.GET['course']
    course_qs =  Course.objects.all()
    course_details = course_qs.filter(name=course_name)
    for course in course_details:
        batches = UpcomingBatch.objects.filter(course_id = course.id).values('id','uc_batch_start_date','course_id')
        for batch in batches:
            batch_start_date = batch['uc_batch_start_date']
            date = datetime.strftime(batch_start_date, '%d-%b-%Y')
            batch_list.append(str(date) + '#' + str(batch['id']))

    if len(batch_list) == 0:
        batch_list.append('empty')
    td = set(batch_list)
    result = '''{}'''.format(list(td))
    return HttpResponse(result)


def load_trainees_ajax(request):
    """
       :param request: Ajax Request
       :return: returns a HttpResponse of selected batch trainee details
    """
    print(request.GET['batch'])
    batch_id =  request.GET['batch']
    trainees = Trainee.objects.filter(batch_id = batch_id)
    cd = set(trainees.values_list('name', flat=True).distinct())
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_selected_trainee_details_ajax(request):
    """
       :param request:Ajax request
       :return: returns a HttpResponse of selected trainee's details
    """
    data = []
    print(request.GET['trainee'])
    trainee = (request.GET['trainee'])
    selected_trainee = Trainee.objects.get(name=trainee)
    trainee_id = selected_trainee.id
    email = selected_trainee.email
    contact = selected_trainee.contact
    course = selected_trainee.course
    batch = selected_trainee.batch
    batch_id = (request.GET['batch'])
    ts_qs = TraineeFees.objects.all()
    
    try:
        ts_fees = ts_qs.filter(name_id=trainee_id, batch_id= batch_id).latest('created_at')
        print(ts_fees)
        print(ts_fees.total_fees_paid)
        print(ts_fees.balance_fee)
        total_fees_paid = ts_fees.total_fees_paid
        balance_fee = ts_fees.balance_fee
    except:
        total_fees_paid = 0
        balance_fee = 0

    print(trainee_id,email,contact,course, total_fees_paid, balance_fee)
    data.append(email)
    data.append(',')
    data.append(contact)
    data.append(',')
    data.append(course)
    data.append(',')
    data.append(batch)
    data.append(',')
    data.append(total_fees_paid)
    data.append(',')
    data.append(balance_fee)

    return HttpResponse(data)


def load_selected_trainer_course_ajax(request):
    """
       :param request: Ajax Request
       :return: returns a HttpResponse of selected trainer course details
    """
    trainer_list = []
    # print(request.GET['trainer'])
    trainer = (request.GET['trainer'])
    selected_trainer = Trainer.objects.filter(name=trainer).distinct()
    
    for trainer in selected_trainer:
        trainer_list.append(str(trainer.course) + '#' + str(trainer.course_id)) 

    cd = set(trainer_list)
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_selected_trainer_details_ajax(request):
    """
       :param request: Ajax Request
       :return: returns a HttpResponse of selected trainer details
    """ 
    data = []
    # print(request.GET['trainer'])
    trainer = (request.GET['trainer'])
    selected_trainer = Trainer.objects.filter(name=trainer)
    course = {}
    for trainer in selected_trainer:
        trainer_id = trainer.id
        email = trainer.email
        contact = trainer.contact
        course.update({'course': trainer.course})

    # print(trainer_id,email,contact)
    data.append(email)
    data.append(',')
    data.append(contact)
  
    return HttpResponse(data)


def load_trainer_batch_ajax(request):
    """
       :param request: Ajax Request
       :return: returns a HttpResponse of batch details for the selected trainer
    """
            #import pdb;pdb.set_trace()
    batch_list = []
    user = request.user
    trainer = Trainer.objects.filter(user_profile_id = user.id).values('id')
    # print(trainer)
    course = (request.GET['course'])
    # print(course)
    batch_qs =  Batch.objects.filter(trainer_id = trainer[0]['id'], course_id=course).values('id','name','start_date','end_date','course_id', 'trainer_id','language_id')
    for batch in batch_qs:
        # print(batch)
        batch_list.append(str(batch['name']) + '#' + str(batch['id']))
    cd = set(batch_list)
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_selected_course_batch_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of batch details for the selected trainer and his course
    """
            #import pdb;pdb.set_trace()
    batch_list = []
    trainer = (request.GET['trainer'])
    # print(trainer)
    course = (request.GET['course'])
    # print(course)
    batch_qs =  Batch.objects.filter(trainer_id = trainer, course_id=course).values('id','name','start_date','end_date','course_id', 'trainer_id','language_id')
    for batch in batch_qs:
        # print(batch)
        batch_list.append(str(batch['name']) + '#' + str(batch['id']))
    cd = set(batch_list)
    result = '''{}'''.format(list(cd))
    return HttpResponse(result)


def load_selected_batch_trainees_ajax(request):
    """
       :param request: Ajax request
       :return: returns a HttpResponse of context of details of Trainees in dict format for the selcted batch to attendance page
    """
    trainees_list = []
    batch_id = (request.GET['batch'])
    course_id = (request.GET['course'])
    trainee_qs = Trainee.objects.all()
    trainee_details = trainee_qs.filter(batch_id=batch_id,course_id=course_id).values('id','name','contact','email','course__name', 'batch__name')
    for trainer in trainee_details:
        tr = {}
        tr['id'] = trainer['id']
        tr['name'] = trainer['name']
        tr['contact'] = trainer['contact']
        tr['email'] = trainer['email']
        tr['course_name'] = trainer['course__name']
        tr['batch_name'] = trainer['batch__name']
        trainees_list.append(tr)
    # print(trainees_list)
    return render(request, 'tb_track_app/trainer_template/trainer_attendance.html', {"trainees_list": trainees_list})


def load_selected_batch_traineer_fee_ajax(request):
    """
       :param request: ajax request
       :return: returns a HttpResponse of array list of details of Trainer Fee for the selcted batch
    """
    data = []

    batch = (request.GET['batch'])
    trainer = (request.GET['trainer'])
    selected_trainer = Trainer.objects.get(id=trainer)
    salary_percent = selected_trainer.salary_percent
    contact = selected_trainer.contact
    course__id = selected_trainer.course
    trainee_count = Trainee.objects.filter(batch_id = batch).count()
    course_qs = CourseFees.objects.filter(course_id = course__id).values('id','course_fee','created_at')
    course_fee = course_qs[0]['course_fee']
    # print((trainee_count*course_fee) * (salary_percent/100))
    amount_to_be_paid = ((trainee_count*course_fee) * (salary_percent/100))
    tp_qs = TrainerPayment.objects.all()

    try:
        tp = tp_qs.filter(contact= contact, name=trainer).latest('created_at')
        if amount_to_be_paid > tp.amount_to_be_paid:
            amount_to_be_paid = amount_to_be_paid
        
        total_amount_paid = tp.total_amount_paid
        balance_salary = tp.balance_salary
    except:
        total_amount_paid = 0
        balance_salary = 0

    data.append(amount_to_be_paid)
    data.append(',')
    data.append(total_amount_paid)
    data.append(',')
    data.append(balance_salary)
    print(data)
    return HttpResponse(data)


#send Email from community Form
from django.conf import settings
from django.core.mail import send_mail
import random

def send_email_ajax(request):
    email_to = []
    
    code = random.randint(1000,9999)
    # print "%04d" % r
    print ('{0:04d}'.format(code))
    email_to.append(request.GET['email'])
    subject = "TamilBoomi Community Verification"
    signature = "Regards,"+'\n'+'TamilBoomi Technologies'
    message ='\n' +'\n'+ "This is the test mail sent from TamilBoomi Community."+'\n'+'Enter the below '\
    'code to validate your e-Mail Id' + '\n' +'\n'+ str(code)+'\n' +'\n'+ signature
    print (email_to)
    email_from = settings.EMAIL_HOST_USER
    data = send_mail(subject,message,email_from,email_to)
    print(data)
    return HttpResponse(code)