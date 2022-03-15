#####################################################################
# Copyright 2021 Lakshmi Siddha clinic. All Rights Reserved.
# Owner       :  Lavanya Balaji
# Created Date:  10/12/2021
# Updater     :  Lavanya Balaji
# Updated Date:  10/12/2021
#####################################################################

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from bs4 import BeautifulSoup

#django-summernote
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

# for update and delete data
from django.urls import reverse

class GroupProfile(models.Model):
    group = models.OneToOneField('auth.Group', unique=True,
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = "group_profile"

    def __str__(self):
        return self.group

# profile used for employee signup
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id_field = models.CharField(max_length=100)
    # user_category (Doctor, Therapist, Receptionist, Patient, Common)
    user_category = models.CharField(max_length=100)

    class Meta:
        db_table = '"user_profile"'

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.CharField(max_length=250)
    item_name = models.CharField(max_length=50)
    cost_price = models.IntegerField()
    sell_price = models.IntegerField()
    manufacturer = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.item_name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id= models.CharField(max_length=250)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_item')
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    expiry_date = models.DateField()

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return self.item.item_name

class MD(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"md"'

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_id = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.TextField()
    mobile = models.PositiveIntegerField()
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    specilization = models.CharField(max_length=100)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name

class Therapist(models.Model):
    id = models.AutoField(primary_key=True)
    therapist_id = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.TextField()
    mobile = models.PositiveIntegerField()
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    specilization = models.CharField(max_length=100)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'therpist'

    def __str__(self):
        return self.name

class Receptionist(models.Model):
    id = models.AutoField(primary_key=True)
    receptionist_id=models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.TextField()
    mobile = models.PositiveIntegerField()
    qualification = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'receptionist'

    def __str__(self):
        return self.name

class PatientBasicInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender= models.CharField(max_length=100)
    mobile = models.PositiveIntegerField()
    email = models.EmailField()
    address = models.TextField()
    emergency_contact = models.PositiveIntegerField()
    insurance = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=10)

    class Meta:
        db_table = 'patient_basic_info'

    def __str__(self):
        return self.name

class PatientMedicalInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient_basic_info = models.ForeignKey(PatientBasicInfo, on_delete=models.CASCADE,
                                           related_name='patient_basic_info')
    allergic = models.CharField(max_length=100)
    past_illness = models.CharField(max_length=500)
    past_surgery = models.CharField(max_length=500)
    treatment_for = models.CharField(max_length=500)
    current_medication=models.CharField(max_length=500)

    class Meta:
        db_table = 'patient_medical_info'

    def  __str__(self):
        return self.patient_basic_info.patient_id

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    patient_medical_info = models.ForeignKey(PatientMedicalInfo, on_delete=models.CASCADE,
                                             related_name='patient_medical_info')
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.patient_medical_info.patient_basic_info.patient_id

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    appointment_id = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment_patient')
    receptionist = models.ForeignKey(Receptionist, on_delete=models.CASCADE, related_name='appointment_receptionist')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_doctor')
    # case = models.ForeignKey(case, on_delete=models.CASCADE, related_name='appointment_case')
    appointment_time = models.DateTimeField()
    description = models.TextField()

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return self.patient.patient_medical_info.patient_basic_info.name

class Case(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='case_appointment')
    description = models.CharField(max_length=500, default=None)
    filed_date = models.DateTimeField(auto_now_add=True)
    next_followup_date = models.DateTimeField(default=None, null=True)
    closed_date = models.DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'case'

    def __str__(self):
        return self.appointment.patient.name + ' having ' + self.description

class Report(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='report_case')
    generated_date = models.DateField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        db_table = 'report'

    def __str__(self):
        return self.case

class Bill(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='bill_case')
    amount = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bill_item')
    quantity = models.IntegerField()
    bill_date = models.DateField()
    bill_details = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'bill'

    def __str__(self):
        return self.case.appointment.patient.name

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description=models.TextField()
    image = models.ImageField(upload_to='images', default='default.jpg')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title

    def short_description(self):
        soup = BeautifulSoup(self.description).text
        return soup[:50]
   
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

        
    class Meta:
        db_table = 'comment'

    def __str__(self):
        return '%s' % (self.post.title)

class Bookappointment(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.TextField(null=False)
    address = models.TextField(null=False)
    reason = models.TextField(null=False)
    apptmt_date = models.DateField(null=False)
    first_visit = models.BooleanField(null=False)

    class Meta:
        db_table = 'bookappointment'

        def __str__(self):
            return self.name