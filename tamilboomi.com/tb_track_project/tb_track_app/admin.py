#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Lavanya Balaji
# Created Date:  21/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################

from django.contrib import admin
from tb_track_app.models import *

class CourseAdmin(admin.ModelAdmin):
 list_display = ['id', 'name','language', 'created_at', 'updated_at']

class ProgrammingLanguageAdmin(admin.ModelAdmin):
 list_display = ['id', 'name','created_at', 'updated_at']

class TrainerAdmin(admin.ModelAdmin):
 list_display = ['id', 'name', 'course', 'email', 'contact','language','created_at']

class AttendanceAdmin(admin.ModelAdmin):
 list_display = ['id', 'trainee', 'status', 'created_at']

class TraineeAdmin(admin.ModelAdmin):
 list_display = ['id', 'name', 'email', 'contact','course','batch','created_at','updated_at']

class BatchAdmin(admin.ModelAdmin):
 list_display = ['id', 'language', 'trainer', 'course','start_date','end_date']

class UpcomingBatchAdmin(admin.ModelAdmin):
 list_display = ['id', 'course', 'uc_batch_start_date', 'uc_batch_end_date']

class TraineeEnrollAdmin(admin.ModelAdmin):
 list_display = ['name', 'contact', 'email', 'language','course','notify_future_batch','up_batch']

class MDAdmin(admin.ModelAdmin):
 list_display = ['id', 'name', 'created_at', 'updated_at']

# class CommunityFormAdmin(admin.ModelAdmin):
#     list_display = ['id','fullname','email','course','phone']

class CommunityFormAdmin(admin.ModelAdmin):
 list_display = ['id', 'first_name', 'last_name', 'technology','hearus','email','code','phone']



admin.site.register(ProgrammingLanguage,ProgrammingLanguageAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(UpcomingBatch,UpcomingBatchAdmin)
admin.site.register(MD,MDAdmin)
admin.site.register(Trainer,TrainerAdmin)
admin.site.register(Trainee,TraineeAdmin)
admin.site.register(Batch,BatchAdmin)
admin.site.register(TraineeEnroll,TraineeEnrollAdmin)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(AttendanceReport)
# admin.site.register(CommunityForm,CommunityFormAdmin)
admin.site.register(CommunityForm)

admin.site.site_header = 'TamilBoomi'