#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Suganya Muthusamy
# Updated Date:  18/11/2021
#####################################################################

from django.shortcuts import render,redirect
from tb_track_app.forms.md_forms import md
from django.http import HttpResponse
from tb_track_app.models import *
from datetime import date
from tb_track_app.models import *

from tb_track_app.views.auth_views.auth_views import get_user_category

def md_home(request):
    """
       MD user category home page with charts
       :param request:
       :return: redirects to MD user category's Home page otherwise redirects to Unauthorized page
    """
   
    user_category = get_user_category(request)
    if user_category == 'MD':
        # Fetching All Students under Staff
        trainer_total_count = Trainer.objects.all().count()
        trainee_total_count = Trainee.objects.all().count()
        course_total_count = Course.objects.all().count()
        batch_total_count = Batch.objects.all().count()
        language_total_count = ProgrammingLanguage.objects.all().count()

        attendance_list = []
        trainee_list = []
        trainee_list_attendance_present = []
        trainee_list_attendance_absent = []

        #   to get total programming languages in each course and
        #   total trainee in each course
        course_name_list = []
        course_language_count_list = []
        course_trainee_count_list = []

        course_all = Course.objects.all()
        for course in course_all:
            if course.name not in course_name_list:
                course_name_list.append(course.name)
                course_language_count = Course.objects.filter(name=course.name).count()
                course_language_count_list.append(course_language_count)
                course_trainee_count = Trainee.objects.filter(course__name=course.name).count()
                course_trainee_count_list.append(course_trainee_count)

        # total trainee in each programming language
        total_language_list = []
        trainee_count_list_in_each_language = []

        language_all = ProgrammingLanguage.objects.all()
        for language in language_all:
            if language.name not in total_language_list:
                total_language_list.append(language.name)
                course_all = Course.objects.filter(language__name=language.name)
                for course in course_all:
                    trainee_total_count_in_language = int()
                    trainee_count = Trainee.objects.filter(course__name=course.name).count()
                    trainee_total_count_in_language += int(trainee_count)
                    trainee_count_list_in_each_language.append(trainee_total_count_in_language)

        color_list = ['#B1E278', '#BC4E55', '#5C5A72', '#D5A021', '#EEC643', '#0D21A1',
                      '#E086D3', '#462749', '#00FFCD', '#4ECDC4', '#FF3333', '#4F5B69',
                      '#E78F4B', '#E5E059', '#BC7D38', '#B4B241', '#6C8889',
                      '#C368CA', '#E5625E', '#5F9FBF', '#BDD358']
        context = {

            "trainer_total_count": trainer_total_count,
            "trainee_total_count": trainee_total_count,
            "course_total_count": course_total_count,
            "batch_total_count": batch_total_count,
            "language_total_count": language_total_count,

            "attendance_list": attendance_list,
            "trainee_list": trainee_list,
            "attendance_present_list": trainee_list_attendance_present,
            "attendance_absent_list": trainee_list_attendance_absent,

            "course_name_list": course_name_list,
            "course_language_count_list": course_language_count_list,
            "course_trainee_count_list": course_trainee_count_list,

            "total_language_list": total_language_list,
            # "language_course_all_list":language_course_all_list,
            "trainee_count_list_in_each_language": trainee_count_list_in_each_language,

            "color_list": color_list,

        }

        return render(request, "tb_track_app/md_template/md_home.html",context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def md_create(request):
    """
       :param request:
       :return: redirects to md create page; for Post request, stores the details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        form = md.MdCreateForm(request.POST or None)
        if request.method == "POST":
            if not MD.objects.filter(
                    name =request.POST['name']).exists():
                db = MD()
                db.name = (request.POST['name'])
                db.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data,content_type='text/plain')
        else:
            context['form']= form
            return render(request, "tb_track_app/md_template/md_add_form.html", context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')

def batch_create(request):
    """
       :param request:
       :return: redirects to Batch create page; for Post request, stores the details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context ={}
        if request.method == "POST":
            qs = list(Trainer.objects.filter(name=request.POST['trainer']).values('id','course_id','language_id'))
            # import pdb;
            # pdb.set_trace()
            if not Batch.objects.filter(
                    name =request.POST['batch_name']).exists():
                db_name = Batch()
                db_name.name = (request.POST['batch_name'])
                db_name.trainer_id= qs[0]['id']
                db_name.course_id = qs[0]['course_id']
                db_name.language_id =qs[0]['language_id']
                db_name.start_date = (request.POST['start_date'])
                db_name.end_date = (request.POST['end_date'])
                db_name.save()

                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data,content_type='text/plain')

        else:
            form = md.BatchCreateForm(request.POST or None)
            # print(form)
            context['form']= form
        return render(request,'tb_track_app/md_template/batch_add_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def batch_edit(request,batch_id):
    """
       :param request:
       :return: redirects to Batch edit page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        batch = Batch.objects.get(id=batch_id)
        context = {
            'batch':batch,
            'id':batch_id
        }
        return render (request, 'tb_track_app/md_template/batch_edit_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')

def batch_edit_save(request):
    """
       :param request:
       :return: stores the batch edit details and returns a HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        batch_id = (request.POST['batch_id'])
        if request.method == "POST":
            try:
                batch =  Batch.objects.get(id=batch_id)
                batch.start_date = (request.POST['start_date'])
                batch.end_date = (request.POST['end_date'])
                batch.name = (request.POST['name'])
                batch.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
            except:
                data = 409
                return HttpResponse(data, content_type = 'text/plain')
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def batch_details(request):
    """
       :param request:
       :return: redirects to Batch summary page;
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        batches = Batch.objects.all()
        context = {
            "batches": batches, 
        }
        return render(request, 'tb_track_app/md_template/batch_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def current_batch_details(request):
    """
       :param request:
       :return: redirects to Current Batch summary page;
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        batches =[]
        qs_batch = Batch.objects.filter(end_date__gte=date.today()).values('id','name','start_date','end_date','course_id', 'trainer_id','language_id')

        for qs in qs_batch:
            batch = {}
            batch['id'] = qs['id']
            batch['name'] = qs['name']
            batch['language'] = ProgrammingLanguage.objects.get(id = qs['language_id'])
            batch['course'] = Course.objects.get(id = qs['course_id'])
            batch['id'] = qs['id']
            batch['start_date'] = qs['start_date']
            batch['end_date'] = qs['end_date']
            batch['trainees'] = Trainee.objects.filter(batch = qs['id']).count()
            batch['trainer'] = Trainer.objects.get(id = qs['trainer_id'])
            batches.append(batch)

        context = {"batches": batches,}
        return render(request, 'tb_track_app/md_template/current_batch_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def enroll_details(request):
    """
       :param request:
       :return: redirects to Enroll summary page;
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        trainees_enroll = TraineeEnroll.objects.all()
        context = {
            "trainees_enroll": trainees_enroll,
        }
        return render(request, 'tb_track_app/trainee_template/trainee_enroll_details.html', context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def languages(request):
    """
       :param request:
       :return: redirects to Language create page; for Post request stores the details and returns HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context={}
        language = ProgrammingLanguage.objects.all().order_by('id')
        context={
            'language':language,
        }
        if request.method=="POST":
            if not ProgrammingLanguage.objects.filter(name = request.POST['language']).exists():
                db_name = ProgrammingLanguage()
                db_name.name = (request.POST['language'])
                db_name.save()
                print('succuess')
                data = 200
                return HttpResponse(data, content_type='text/plain')
        else:
            return render(request,'tb_track_app/md_template/programming_language_add_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def language_details(request):
    """
       :param request:
       :return: redirects to Language summary page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        language = ProgrammingLanguage.objects.all().order_by('id')
        context={
            'language':language,
        }
        return render(request,'tb_track_app/md_template/programming_language_details.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def course_add(request):
    """
       :param request:
       :return: redirects to Course create page; for Post request stores the details and returns HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        context={}
        if request.method=="POST":
            db_name = Course()
            db_name.name=(request.POST['name'])
            db_name.language_id=(request.POST['language'])
            db_name.save()
            print('success')
            data = 200 
            return HttpResponse(data,content_type='text/plain')
        else:
            form = md.CourseCreationForm(request.POST or None)
            context['form']= form
        return render(request,'tb_track_app/md_template/course_add_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def course_edit(request):
    """
       :param request:
       :return: redirects to Course Edit page; for Post request stores the details and returns HttpResponse accordingly
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        courses = Course.objects.all().distinct('name')
        languages = ProgrammingLanguage.objects.all()
        context={'courses':courses, 'languages': languages,}
        if request.method=="POST":
            if not Course.objects.filter(language_id = request.POST['language']).exists():
                db_name = Course()
                db_name.name=(request.POST['name'])
                db_name.language_id=(request.POST['language'])
                db_name.save()
                print('success')
                data = 200 
                return HttpResponse(data,content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data,content_type='text/plain')

        return render(request,'tb_track_app/md_template/course_edit_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def course_details(request):
    """
       :param request:
       :return: redirects to Course summary page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        courses = Course.objects.all().order_by('name')
        context={'courses':courses}

        return render(request,'tb_track_app/md_template/course_details.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def course_fee(request):
    """
       :param request:
       :return: redirects to Course fee add page; for Post request stores the details and returns HttpResponse accordingly
    """ 
    user_category = get_user_category(request)
    if user_category == 'MD':
        course_fees = CourseFees.objects.all()
        courses = Course.objects.all().order_by('name').distinct('name')
        context = { 'course_fees': course_fees, 'courses':courses}
        if request.method == "POST":
            if not CourseFees.objects.filter(course= request.POST['course']).exists():
                db = CourseFees()
                db.course_id = request.POST['course']
                db.course_fee = request.POST['course_fee']
                db.save()
                print('success')
                data = 200 
                return HttpResponse(data,content_type='text/plain')
            else:
                data = 409
                return HttpResponse(data,content_type='text/plain')

        return render(request,'tb_track_app/md_template/course_fee_add_form.html',context)
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')


def batch_upcoming_add(request, batch_id):
    """
       :param request:
       :return: redirects to Batch edit page
    """   
    user_category = get_user_category(request)
    if user_category == 'MD':
        batch = Batch.objects.get(id=batch_id)
        db = UpcomingBatch()
        db.uc_batch_start_date = batch.start_date
        db.uc_batch_end_date = batch.end_date
        db.course = batch.course
        try:
            db.save()
            print('success')
            data = 200 
            return HttpResponse(data,content_type='text/plain')
        except:
            data = 409
            return HttpResponse(data,content_type='text/plain')
    else:
        return render(request, 'tb_track_app/accounts/unauthorized.html')
   