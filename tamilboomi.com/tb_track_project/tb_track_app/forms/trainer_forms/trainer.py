#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  15/11/2021
#####################################################################

from django import forms
from django.forms import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth.models import User, Group
from tb_track_app.models import *

class TrainerCreateForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainerPaymentAddForm(forms.ModelForm):
    class Meta:
        model = TrainerPayment
        fields = '__all__'



