#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  15/11/2021
#####################################################################

from django import forms
from django.db.models import fields
from tb_track_app.models import *
from tb_track_app.models import Trainee,TraineeEnroll

class TraineeCreateForm(forms.ModelForm):
    class Meta:
        model = Trainee
        fields = '__all__'
    
    

class TraineeEnrollForm(forms.ModelForm):
    class Meta:
        model = TraineeEnroll
        fields = '__all__'


class TraineeFeesAddForm(forms.ModelForm):
    class Meta:
        model = TraineeFees
        fields = '__all__'