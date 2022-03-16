from django.db import models
import datetime

# Create your models here.
DEBIT_OPTIONS = (
    ("Auto Refill", "Auto Refill"),
    ("Manual Recharge", "Manual Recharge"),
    ("Digital", "Digital"),
    ("FSE1", "FSE1"),
    ("FSE2", "FSE2"),
    ("FSE3", "FSE3"),
    ("FSE4", "FSE4"),
)

CREDIT_OPTIONS = (
    ("Digital", "Digital"),
    ("G-Pay", "G-Pay"),
    ("Bank", "Bank"),
    ("Cash", "Cash"),
)

FSE_OPTIONS = (
    ("FSE1", "FSE1"),
    ("FSE2", "FSE2"),
    ("FSE3", "FSE3"),
    ("FSE4", "FSE4"),
)

STAFF_CASH = (
    ("Salaey", "Salary"),
    ("Advance", "Advance"),
    ("Bonus", "Bonus"),
    ("Commision", "Commision"),
)

class ClientProfile(models.Model):
    id = models.AutoField(primary_key=True)
    record_name = models.CharField(max_length=100)
    actual_name = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=12)
    secondary_contact = models.CharField(max_length=12, blank=True, null=True)
    address = models.TextField(default=None, blank=True, null=True)
    area_name = models.CharField(max_length=100)
    area_code = models.CharField(max_length=50, blank=True, null=True)
    pending_payment= models.DecimalField(max_digits=50, decimal_places=2)
    
    class Meta:
        db_table = '"Client"'

    def __str__(self):
        return self.actual_name


class DebitTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(ClientProfile, default= None, on_delete=models.SET_DEFAULT)
    date = models.DateField()
    debit_amount = models.DecimalField(max_digits=50, decimal_places=2)
    debit_option = models.CharField(max_length=50, choices=DEBIT_OPTIONS)
    open_balance = models.DecimalField(max_digits=50, decimal_places=2)
    close_balance = models.DecimalField(max_digits=50, decimal_places=2)
    sales_commision = models.DecimalField(max_digits=50, decimal_places=2)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    collected_on = models.DateField(null=True, blank=True)

    class Meta:
        db_table = '"Debit"'

    def __str__(self):
        return self.client


class CreditTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(ClientProfile, default= None, on_delete=models.SET_DEFAULT)
    date = models.DateField()
    credit_amount = models.DecimalField(max_digits=50, decimal_places=2)
    credit_option = models.CharField(max_length=50, choices=CREDIT_OPTIONS)
    open_balance = models.DecimalField(max_digits=50, decimal_places=2)
    close_balance = models.DecimalField(max_digits=50, decimal_places=2)
    remarks = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = '"Credit"'

    def __str__(self):
        return self.client


class SalesTranscations(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(ClientProfile, default=1, on_delete=models.SET_DEFAULT)
    debit =  models.ForeignKey(DebitTransaction, default=1, on_delete=models.SET_DEFAULT)
    credit =  models.ForeignKey(CreditTransaction, default=1, on_delete=models.SET_DEFAULT)
    open_balance = models.DecimalField(max_digits=50, decimal_places=2)
    close_balance = models.DecimalField(max_digits=50, decimal_places=2)
    sales_commision = models.DecimalField(max_digits=50, decimal_places=2)
    remarks = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = '"Sales"'

    def __str__(self):
        return self.client


class MCashTranscations(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    mcash_amount = models.DecimalField(max_digits=50, decimal_places=2)
    sales_commision = models.DecimalField(max_digits=50, decimal_places=2)
    retailer_commision = models.DecimalField(max_digits=50, decimal_places=2)
    distributor_commision = models.DecimalField(max_digits=50, decimal_places=2)
    opening_balance = models.DecimalField(max_digits=50, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        db_table = '"MCash"'

    def __str__(self):
        return self.date


class StaffProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=12)
    address = models.CharField(max_length=500)
    joined_on = models.DateField()
    salary = models.DecimalField(max_digits=50, decimal_places=2)
    area = models.CharField(max_length=500)
    fse = models.CharField(max_length=20, choices=FSE_OPTIONS)
    class Meta:
        db_table = '"Staff"'

    def __str__(self):
        return self.name


class StaffCashTransation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(StaffProfile,default=1, on_delete=models.SET_DEFAULT)
    date = models.DateField()
    cash_paid = models.DecimalField(max_digits=50, decimal_places=2)
    balance_salary = models.DecimalField(max_digits=50,decimal_places=2)
    reason = models.CharField(max_length=12, choices=STAFF_CASH, default=1)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"StaffCash"'

    def __str__(self):
        return self.name


class AutoRefillTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    fse_msisdn = models.CharField(max_length=50)
    fse_name= models.CharField(max_length=50)
    retailer_msisdn = models.CharField(max_length=50)
    profile = models.ForeignKey(ClientProfile, on_delete=models.SET_NULL, blank=True, null=True)
    retailer_name = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=50)
    auto_refill_date = models.DateTimeField()
    transferred_amount = models.DecimalField(max_digits=50, decimal_places=2)
    collectable_amount = models.DecimalField(max_digits=50, decimal_places=2)
    status = models.CharField(max_length=50)
    collected_on = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=100,blank=True, null=True)
    
    class Meta:
        db_table = '"Auto_Refill"'

    def __str__(self):
        return self.retailer_name
