#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Lavanya Balaji
# Created Date:  21/10/2021
# Updater     :  Arun Madhu
# Updated Date:  15/11/2021
#####################################################################

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# for update and delete data
from django.urls import reverse

class GroupProfile(models.Model):
    group = models.OneToOneField('auth.Group', unique=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "group_profile"
        # ordering = ['employee_id']

    def __str__(self):
        return self.group

# profile used for employee signup
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id_field = models.CharField(max_length=100)
    # user_category ( MD, Trainer, Trainee, CommonUser)
    user_category = models.CharField(max_length=100)

    class Meta:
        db_table = '"user_profile"'
        # ordering = ['user_id']
        # abstract = True

    def __str__(self):
        return self.user_id_field


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class ProgrammingLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"programming_language"'

    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"courses"'

    def __str__(self):
        return self.name


class UpcomingBatch(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uc_batch_start_date = models.DateTimeField()
    uc_batch_end_date = models.DateTimeField()

    class Meta:
        db_table = '"upcoming_batch"'

    def __str__(self):
        return str(self.uc_batch_start_date)

class MD(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"md"'

    def __str__(self):
        return self.name

class Trainer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField()
    contact = models.CharField(max_length=12)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    salary_percent = models.IntegerField(default=0, blank=True)
    variable_salary_percent = models.IntegerField(default=0, blank=True)
    fixed_monthly_salary = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"trainer"'

    def __str__(self):
        return self.name

class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = '"batch"'

    def __str__(self):
        return str(self.name)

class Trainee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default=True)
    contact = models.CharField(max_length=12)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"trainee"'

    def __str__(self):
        return self.name

class TraineeEnroll(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.EmailField()
    language = models.ForeignKey(ProgrammingLanguage, models.CASCADE, null=True)
    course = models.ForeignKey(Course, models.CASCADE)
    notify_future_batch = models.BooleanField(null=True)
    up_batch = models.ForeignKey(UpcomingBatch, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = '"trainee_enroll"'

    def __str__(self):
        return self.name

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    language = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"attendence"'

    def __str__(self):
        return str(self.id)

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    status_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)

    class Meta:
        db_table = '"attendence_report"'

    def __str__(self):
        return str(self.id)


class TraineeFees(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    contact = models.CharField(max_length=12)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, models.CASCADE, null=True)
    amount_paid = models.PositiveIntegerField(null=True)
    total_fees_paid = models.PositiveIntegerField(null=True)
    balance_fee = models.PositiveIntegerField(null=True)
    date = models.DateField()
    remarks = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = '"trainee_fees"'

    def __str__(self):
        return str(self.name)

TRAINER_PAY = (
    ("Salary", "Salary"),
    ("Advance", "Advance"),
    ("Bonus", "Bonus"),
    ("Commision", "Commision"),
)

class TrainerPayment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    contact = models.CharField(max_length=12)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, models.CASCADE, null=True)
    amount_to_be_paid = models.PositiveIntegerField(null=True)
    amount_paid = models.PositiveIntegerField(null=True)
    payment_reason = models.CharField(max_length=12, choices=TRAINER_PAY, default=1)
    balance_salary = models.PositiveIntegerField(null=True)
    total_amount_paid = models.PositiveIntegerField(null=True)
    date = models.DateField()
    remarks = models.TextField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = '"trainer_payment"'

    def __str__(self):
        return str(self.name)


class CourseFees(models.Model):
    id = models.AutoField(primary_key=True)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    course_fee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"course_fees"'

    def __str__(self):
        return str(self.course)


class BatchFees(models.Model):
    id = models.AutoField(primary_key=True)
    course_fee= models.ForeignKey(CourseFees, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    total_fee_batch = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"batch_fees"'

    def __str__(self):
        return str(self.batch)


class CommunityForm(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    technology = models.ForeignKey(Course, on_delete=models.CASCADE)
    hearus = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    class Meta:
        db_table = '"community_form"'


    def __str__(self):
        return self.email

    def fullname(self):
        return self.firstname+" "+self.lastname
# class CommunityForm(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     technology = models.CharField(max_length=100)
#     hearus = models.CharField(max_length=100)
#     email = models.EmailField()
#     code = models.CharField(max_length=5)
#     phone = models.IntegerField()

#     class Meta:
#         db_table = '"community_form"'
    
#     def __str__(self):
#         return str(self.email)

