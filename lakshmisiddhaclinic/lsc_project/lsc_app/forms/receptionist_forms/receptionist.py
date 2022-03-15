#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Lavanya
# Updated Date:  11/12/2021
#####################################################################

from django import forms

from lsc_app.models import *
class ReceptionistCreateForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = '__all__'