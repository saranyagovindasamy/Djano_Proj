#####################################################################
# Copyright 2021 Lakshi Siddha Clinic. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  11/12/2021
# Updater     :  Arun Madhu
# Updated Date:  11/12/2021
#####################################################################

from django import forms 

from lsc_app.models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class BlogCreateForm(forms.ModelForm):
    description = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea
    class Meta:
        model = Blog
        fields = '__all__'
     
    
