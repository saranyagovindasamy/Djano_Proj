#####################################################################
# Copyright 2021 Lakshmi Siddha clinic. All Rights Reserved.
# Owner       :  Lavanya Balaji
# Created Date:  10/12/2021
# Updater     :  Lavanya Balaji
# Updated Date:  10/12/2021
#####################################################################

from django.contrib import admin
from .models import *
#  UserProfile, GroupProfile, Item, Stock, Doctor, Therapist,\
    # Receptionist, Patient, Appointment, Case, Report, Bill, Blog, Comment


# from .models import UserProfile, GroupProfile, Item, Stock, MD, Doctor, Therapist,\
    # Receptionist, Patient, Appointment, Case, Report, Bill 

from django_summernote.admin import SummernoteModelAdmin
from .models import Blog




    # Receptionist, Patient, Appointment, Case, Report, Bill , Blog, PatientMedicalInfo, PatientBasicInfo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_id_field', 'user_category']

class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ['group']

class ItemAdmin(admin.ModelAdmin):
   list_display = ['id', 'item_id','item_name', 'cost_price', 'sell_price','manufacturer',
                 'description']

class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock_id','item', 'quantity', 'purchase_date', 'expiry_date']

class MDAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id','doctor_id','name', 'profile_pic', 'address', 'mobile', 'qualification',
                    'gender', 'specilization', 'user_profile']

class TherapistAdmin(admin.ModelAdmin):
    list_display = ['id','therapist_id','name', 'profile_pic', 'address', 'mobile', 'qualification',
                    'gender', 'specilization', 'user_profile']

class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ['id','receptionist_id','name', 'profile_pic', 'address', 'mobile', 'qualification',
                    'gender', 'user_profile']

class PatientBasicInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_id', 'name', 'dob', 'age', 'gender', 'mobile', 'email', 'address',
                    'emergency_contact', 'insurance', 'aadhar', 'blood_group']

class PatientMedicalInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_basic_info','allergic', 'past_illness', 'past_surgery',
                    'treatment_for', 'current_medication']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient_medical_info', 'user_profile']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id','patient', 'receptionist', 'doctor', 'appointment_time',
                    'description']

class CaseAdmin(admin.ModelAdmin):
    list_display = ['id','appointment', 'description', 'filed_date', 'next_followup_date',
                    'closed_date']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'case', 'generated_date', 'description']

class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'case', 'amount', 'item', 'quantity', 'bill_date',
                    'bill_details', 'is_paid']

class BlogAdmin(SummernoteModelAdmin):
    list_display = ['id','title','short_description','image','created_date','updated_date']
    ordering = ['-updated_date','-created_date']
  
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name','body','date_added']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(MD, MDAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Receptionist, ReceptionistAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientBasicInfo, PatientBasicInfoAdmin)
admin.site.register(PatientMedicalInfo, PatientMedicalInfoAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment,CommentAdmin)



# Register your models here.
admin.site.site_header = "Lakshmi Siddha Clinic"
admin.site.site_title = "Lakshmi Siddha Clinic"
admin.site.index_title = "Lakshmi Siddha Clinic Administration"
admin.site.site_header = "Lakshmi Siddha Clinic"
admin.site.site_title = "Lakshmi Siddha Clinic"
admin.site.index_title = "Lakshmi Siddha Clinic Administration"


