#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Lavanya Balaji
# Created Date:  21/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

from tb_track_app.views.common_views import common_views
from tb_track_app.views.ajax_views import ajax_views as ajax
from tb_track_app.views.md_views import md, test
from tb_track_app.views.trainer_views import trainer
from tb_track_app.views.trainee_views import trainee
from tb_track_app.views.auth_views.auth_views import signup,login_user,user_login_summary,change_password
from tb_track_app.views.api_views.api import *


urlpatterns = [
    
    re_path(r'^favicon\.ico$', favicon_view),
    path('', common_views.home, name='home'),
    path('home/', common_views.home, name='home'),

    # common views
    path('courses/', common_views.courses, name='courses'),
    path('fullstack/', common_views.fullstack, name='fullstack'),
    path('snowflake/', common_views.snowflake, name='snowflake'),
    path('bigdata/', common_views.bigdata, name='bigdata'),
    path('devops/', common_views.devops, name='devops'),
    path('enroll/', common_views.enroll, name='enroll'),
    path('faculties/', common_views.faculties, name='faculties'),
    path('communityform/',common_views.communityform,name='communityform'),
 
    # User Login/Logout
    path('userhome/', common_views.switch_user_view, name='userhome'),
    path(r'signup/', signup, name='signup'),
    path('login/',login_user,name="login"),
    path('reset-password/',change_password,name="reset-password"),
    path(r'login-summary/', user_login_summary, name='login-summary'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name="tb_track_app/accounts/logged_out.html"), name="logout"),

    # MD Views URL
    path('test/home', test.test_home, name='test-home'),
    path('md/new', md.md_create, name='md-new'),
    path('md/home', md.md_home, name='md-home'),
    path('enroll/summary', md.enroll_details, name='enroll-summary'),
    path('batch/details', md.batch_details, name='batch-details'),
    path('language',md.languages,name='language'),
    path('language/summary',md.language_details,name='language_details'),
    path('course/add',md.course_add,name='course_add'),
    path('course/fee',md.course_fee,name='course-fee'),
    path('course/edit',md.course_edit,name='course_edit'),
    path('course/details',md.course_details,name='course_details'),
    path('batch/new', md.batch_create, name='batch-new'),
    path('batch/edit/<batch_id>', md.batch_edit, name='batch-edit'),
    path('batch/upcoming/<batch_id>', md.batch_upcoming_add, name='batch-upcoming'),
    path('batch/current', md.current_batch_details, name='batch-current'),
      
    # Trainer Views URL
    path('trainer/home', trainer.trainer_home, name='trainer-home'),
    path('trainer/details', trainer.trainer_details, name='trainers-details'),
    path('trainer/new', trainer.trainer_create, name='trainer-new'),
    path('trainer/attedance', trainer.trainer_attendance, name='trainer-attendance'),
    path('trainer/attedance-summary', trainer.trainer_attendance_summary, name='trainer-attendance-summary'),
    path('trainer/pay', trainer.trainer_payment_add, name='trainer-add-pay'),
    path('trainer/paydetails', trainer.trainer_payment_details, name='trainer-payment-details'),

    #Trainee Views URL
    path('trainee/home', trainee.trainee_home, name='trainee-home'),
    path('trainee/new', trainee.trainee_create, name='trainee-new'),
    path('trainee/details', trainee.trainee_details, name='trainees-details'),
    path('trainee/fees', trainee.trainee_fees_add, name='trainee-add-fee'),
    path('trainee/feesdetails', trainee.trainee_fees_details, name='trainee-fees-details'),

    # Ajax views URL's
    path(r'load_languages_ajax/', ajax.load_languages_ajax, name='load_languages_ajax'),
    path(r'load_courses_md_ajax/', ajax.load_courses_md_ajax, name='load_courses_md_ajax'),
    path(r'load_trainer_md_ajax/', ajax.load_trainer_md_ajax, name='load_trainer_md_ajax'),
    path(r'load_language_ajax/', ajax.load_language_ajax, name='load_language_ajax/'),
    path(r'load_trainerbatch_ajax/', ajax.load_trainerbatch_ajax, name='load_trainerbatch_ajax/'),
    path(r'load_trainees_ajax/', ajax.load_trainees_ajax, name='load_trainees_ajax/'),
    path(r'load_enroll_batch_ajax/', ajax.load_enroll_batch_ajax, name='load_enroll_batch_ajax/'),
    path(r'load_selected_trainee_details_ajax/', ajax.load_selected_trainee_details_ajax, name='load_selected_trainee_details_ajax/'),
    path(r'load_selected_trainer_details_ajax/', ajax.load_selected_trainer_details_ajax, name='load_selected_trainer_details_ajax/'),
    path(r'load_selected_trainer_course_ajax/', ajax.load_selected_trainer_course_ajax, name='load_selected_trainer_course_ajax/'),
    path(r'load_selected_course_batch_ajax/', ajax.load_selected_course_batch_ajax, name='load_selected_course_batch_ajax/'),
    path(r'load_trainer_batch_ajax/', ajax.load_trainer_batch_ajax, name='load_trainer_batch_ajax/'),
    path(r'load_selected_batch_traineer_fee_ajax/', ajax.load_selected_batch_traineer_fee_ajax, name='load_selected_batch_traineer_fee_ajax/'),
    path(r'load_selected_batch_trainees_ajax/', ajax.load_selected_batch_trainees_ajax, name='load_selected_batch_trainees_ajax/'),
    path(r'load_selected_category_users_ajax/', ajax.load_selected_category_users_ajax, name='load_selected_category_users_ajax/'),
    path(r'suggest_username_ajax/', ajax.suggest_username_ajax, name='suggest_username_ajax/'),
    path(r'load_batch_ajax/', ajax.load_batch_ajax, name='load_batch_ajax/'),
    path(r'send_email_ajax/', ajax.send_email_ajax, name='send_email_ajax/'),
   
    
    #API View
     path('groupprofile_api/',groupprofile_api, name='groupprofile_api'),
     path('user_api/',userprofile_api, name='userprofile_api'),
     path('program_api/',programmingLanguage_api, name='programmingLanguage_api'),
     path('course_api/',course_api, name='course_api'),
     path('upcomingbatch_api/',upcomingbatch_api, name='upcomingBatch_api'),
     path('md_api/',md_api, name='md_api'),
     path('trainer_api/',trainer_api, name='trainer_api'),
     path('batch_api/',batch_api, name='batch_api'),
     path('trainee_api/',trainee_api, name='trainee_api'),
     path('traineeenroll_api/',traineeenroll_api, name='traineeenroll_api'),
     path('attendance_api/',attendance_api, name='attendance_api'),
     path('attendancereport_api/',attendancereport_api, name='attendancereport_api'),
  


]
