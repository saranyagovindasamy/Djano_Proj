#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  29/11/2021
# Updater     :  Arun Madhu
# Updated Date:  29/11/2021
#####################################################################
from django.urls import path, re_path
# from lsc_app.views.common_views import common_views
from django.conf import settings
from django.conf.urls.static import static
from lsc_app.views.common_views.common_views import *
from lsc_app.views.md_views.md import *
from lsc_app.views.md_views.test import *
from lsc_app.views.auth_views.auth_views import *
from lsc_app.views.doctor_views.doctor import doctor_create, doctor_summary, doctorappoint_summary, doctor_home
from lsc_app.views.therapist_views.therapist import therapist_create, therapist_summary
from lsc_app.views.receptionist_views.receptionist import receptionist_create, receptionist_summary, recep_home, recepappoint_summary, appoint_update
from lsc_app.views.patient_views.patient import patient_create, patient_add, patient_medical, patient_summary
from lsc_app.views.md_views.blog import *
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from lsc_app.views.ajax_views import ajax_views as ajax
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static



favicon_view = RedirectView.as_view(url='/static/lsc_app/lsc_images/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('specialities/',specialities,name='specialities'),
    path('treatments/',treatments,name='treatments'),
    path('blog/',blog,name='blog'),
    # path('blog/<int:pk>/',  BlogDetailView.as_view(),name='blog-detail'),
    path('contactus/',contactus,name='contactus'),
    path('bookanappointment/',bookanappointment,name='bookanappointment'),

    # User Login/Logout
    path('userhome/', switch_user_view, name='userhome'),
    path(r'signup/', signup, name='signup'),
    path('login/',login_user,name="login"),
    path('reset-password/',change_password,name="reset-password"),
    path(r'login-summary/', user_login_summary, name='login-summary'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name=
                   "lsc_app/accounts/logged_out.html"), name="logout"),
    

    # md user urls
    path('test/home', test_home, name='test-home'),
    path('md/new', md_create, name='md-new'),
    path('md/home', md_home, name='md-home'),
    path('recep/home', recep_home, name='receptionist-home'),
    path('md/doctorhome', doctor_home, name='doctor-home'),
    path('md/blog',blog_list, name='blog-list'),
    
   
    # blog
    # path('blog/<str:username>/', blog_user_post, name='user-posts'),
    path('blog/<int:id>/', blog_detail_view, name='blog-detail'),
    path('post/<int:id>/', post_view, name='post-detail'),
    path('blog/edit/<int:id>/', blog_edit, name='blog-edit'),
    path('blog/delete/<int:id>/', blog_delete, name='blog-delete'),
    path('summernote/', include('django_summernote.urls')),
    path('md/blog/new',blog_create, name='blog-create'),
    path('md/doctor', doctor_create, name = 'addDoctor'),
    path('md/doctorsummary', doctor_summary, name = 'doctorsummary'),
    path('md/therapist', therapist_create, name = 'addTherapist'),
    path('md/therapistsumm', therapist_summary, name = 'therapistsumm'),
    path('md/receptionist', receptionist_create, name = 'addReceptionist'),
    path('md/receptionistsumm', receptionist_summary, name = 'recepsummary'),
    path('patient/addbasic',patient_create,name='addpatient'),
    path('patient/addpatient',patient_add,name='addpatientdetails'),
    path('patient/addmedical',patient_medical,name='addmedical'),
    path('Patientsummary/',patient_summary, name='patientsumm'),
    path('md/appointsumm', appointment_summary, name = 'apptmtsumm'),
    path('md/appointsummrecep', recepappoint_summary, name = 'apptmtsummrecep'),
    path('md/appointupdate', appoint_update, name = 'appoint_update'),
    path('md/doctorappointments', doctorappoint_summary, name = 'drappointsummary'),
    # ajax views urls

    path(r'load_selected_category_users_ajax/', ajax.load_selected_category_users_ajax, name='load_selected_category_users_ajax/'),
    path(r'suggest_username_ajax/', ajax.suggest_username_ajax, name='suggest_username_ajax/'),
    path('blog-comment',blog_comment,name='blog-comment'),
    path(r'load_blog_images_ajax/', ajax.load_blog_images_ajax, name='load_blog_images_ajax/'),
] 
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static( settings.MEDIA_URL, document_root= settings.MEDIA_ROOT )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)