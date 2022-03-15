#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Saranya Arun
# Created Date:  13/12/2021
# Updater     :  Saranya Arun
# Updated Date:  13/12/2021
#####################################################################

from django.contrib.auth import login, authenticate
from lsc_app.models import *
from django.shortcuts import render, HttpResponse, redirect
from lsc_app.models import *
from lsc_app.views.auth_views.auth_views import get_user_category
from lsc_app.forms.blog_forms.blog import *
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView 
from django.core.paginator import Paginator
from django.shortcuts import (get_object_or_404, render,HttpResponseRedirect)
from django.utils import timezone
from django.contrib import messages


def blog_list(request):
    blog_details = Blog.objects.all().order_by("-created_date")
    paginator = Paginator(blog_details,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'blog_details':blog_details,
    'page_obj':page_obj}
    return render(request,"lsc_app/md_template/blog_list.html",context)


def blog_create(request):

    if request.method == 'POST':
        print(request.POST['blog_content'])
        print(request.POST['blog_title'])
        title = request.POST['blog_title']
        content = request.POST['blog_content']
        if title != False and content !=False:
            try:
                # print (title, content)
                db = Blog()
                db.title = title
                db.description = content
                # db.inside_image = description
                try:
                    image = request.FILES['blog_image']
                except:
                # MultiValueDictKeyError happens when a key doesn't exist
                    image = 'images/default.jpg'
                db.image = image
                db.save()
                data = 200
            except:
                data = 500
        else:
            data = 500

        return HttpResponse(data, content_type = 'text/plain')
    else:
        form = BlogCreateForm
        context={'form':form}
        return render(request,"lsc_app/md_template/blog_create_form.html",context)


def blog_user_post(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        blog_details = Blog.objects.filter(blog_user = user_id ).order_by("-blog_created_date")
        context={'blog_details':blog_details}
        return render(request,"lsc_app/blog/user_posts.html",context)


def blog_detail_view(request, id):
    print (id)
    post = Blog.objects.filter(id = id)[0]
    comment = Comment.objects.filter(post_id = id)
    context = {
        'post_id' : id,
        'post':post,
        'comment':comment,
    }
    return render(request,"lsc_app/blog/blog_detail_view.html",context)
    

from django.utils import timezone
def blog_edit(request, id):
    print(id)
    post = Blog.objects.filter(id = id)[0]
    if request.method == "POST":
            if request.POST['blog_title'] and request.POST['blog_description']:
                print(request.POST['blog_description'])
                obj = Blog.objects.get(id= id)
                obj.title = request.POST['blog_title']
                obj.description = request.POST['blog_description']
                obj.inside_image = request.POST['blog_description']
                obj.updated_date = timezone.datetime.now()
                obj.created_date = obj.created_date
                obj.save()
                return render(request, 'lsc_app/md_template/blog_create_form.html', {'obj':obj})

            else:
                return render(request, 'lsc_app/blog/blog_detail_view.html', {'error':'All fields are required'})
    else:
        form = BlogCreateForm
        context = {
            'form':form,
            'post':post
        }
        return render(request,"lsc_app/md_template/blog_edit_form.html", context)
        

def blog_delete(request, id):
    print(id)
    task=Blog.objects.filter(id = id)[0]
    task.delete()
    messages.success(request, "Post Deleted Successfully")
    return render(request,"lsc_app/md_template/blog_list.html",messages)