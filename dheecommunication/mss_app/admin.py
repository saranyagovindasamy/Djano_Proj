from django.contrib import admin
from mss_app.form import ClientProfileCreateForm
from mss_app.models import *

# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(DebitTransaction)
admin.site.register(CreditTransaction)
admin.site.register(SalesTranscations)