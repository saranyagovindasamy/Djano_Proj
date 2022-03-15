#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  29/11/2021
# Updater     :  Arun Madhu
# Updated Date:  29/11/2021
#####################################################################

from django.shortcuts import render, redirect
from django.http import HttpResponse
from lsc_app.models import Blog, Comment, Bookappointment
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User

def home(request):
    return render(request,'lsc_app/common_template/home.html')



def specialities(request):
    return render(request,'lsc_app/common_template/specialities.html')

def treatments(request):
    return render(request,'lsc_app/common_template/treatments.html')

def contactus(request):
    return render(request,'lsc_app/common_template/contactus.html')

def blog(request):
    blog_details = Blog.objects.all().order_by("-updated_date","-created_date")

    print(Blog.objects.all().count())
    paginator = Paginator(blog_details,6)
    print (paginator)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context={'blog_details':blog_details,
    'page_obj':page_obj}
    return render(request,'lsc_app/common_template/blog.html',context)


def post_view(request, id):
    print('post_view')
    print (id)
    post = Blog.objects.filter(id = id)[0]
    comment = Comment.objects.filter(post_id = id)
    print(post)
    print(comment)
    context = {
        'post_id' : id,
        'post':post,
        'comment':comment,
    }
    return render(request,"lsc_app/common_template/blog_detail.html",context)

def blog_comment(request):
    if request.method == "POST":
        print(request.POST['comments'], request.POST['id'])
        id = request.POST['id']
        db = Comment()
        db.post = Blog.objects.get(id = id)
        db.name = 'anonymous'
        db.body = request.POST['comments']
        db.save()
        result = '200'
        return HttpResponse(result)


def bookanappointment(request):
    if request.method == "POST":
        data = Bookappointment()
        data.name = request.POST['name']
        data.mobile = request.POST['contact']
        data.address = request.POST['address']
        data.apptmt_date = request.POST['date']
        if request.POST['first_visit'] == "yes":
          data.first_visit = True
        else:
          data.first_visit = False
        data.reason = request.POST['reason']
        data.save()
        data1 = 200
        return HttpResponse(data1,content_type='text/plain')

    return render(request,'lsc_app/common_template/bookanappointment.html')

def appointment_summary(request):
  data = Bookappointment.objects.all()
  context = {'data':data}
  return render(request,'lsc_app/common_template/appointment_summary.html', context)

def login(request):
    return render(request,'lsc_app/accounts/login.html')


def get_user_category(request):
    group = Group.objects.filter(user=request.user)
    if len(group) == 0:
        return "None"
    if group[0].name == "MD" or group[0].name == 'Doctor' or group[0].name == \
            'Therapist' or group[0].name == 'Receptionist' or group[0].name == \
            "Patient":
        return "Admin"

def home(request):
    print(request.user)
    # if request.user.is_authenticated:
    #   user_category = get_user_category(request)
    #   if user_category == 'Admin' or user_category== 'MD':
    #     return render(request, 'lsc_app/md_template/admin_home.html')
    return render(request, 'lsc_app/common_template/home.html')

def switch_user_view(request):
    if request.user.is_authenticated:
        user_category = request.user.userprofile.user_category
        print (user_category)
        print(Group.objects.all())
        print (Group.objects.filter(id=user_category))
        user_group = (Group.objects.filter(id=user_category)[0]).name
        print(user_group)
        if user_group == "MD":
            print("redirects to md-home")
            return redirect('md-home')
        elif user_group == "Doctor":
            return redirect('doctor-home')
        elif user_group == "Therapist":
            return redirect('therapist-home')
        elif user_group == "Receptionist":
            return redirect('receptionist-home')
        elif user_group == "Patient":
            return redirect('patient-home')

        else:
            return render(request,'lsc_app/index/home.html')
    return redirect('login')
