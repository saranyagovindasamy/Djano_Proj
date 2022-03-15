#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Arun Madhu
# Updated Date:  11/12/2021
#####################################################################

from django import forms 

from lsc_app.models import *

class MdCreateForm(forms.ModelForm):
    class Meta:
        model = MD
        fields = '__all__'
    
