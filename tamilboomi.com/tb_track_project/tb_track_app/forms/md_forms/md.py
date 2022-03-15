#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  15/11/2021
#####################################################################


from django import forms
from tb_track_app.models import *

class MdCreateForm(forms.ModelForm):
    class Meta:
        model = MD
        fields = '__all__'
    

class BatchCreateForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'


class ProgrammingLanguageCreateForm(forms.ModelForm):

    class Meta:
        model= ProgrammingLanguage
        fields='__all__'
    
    
class CourseCreationForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'
