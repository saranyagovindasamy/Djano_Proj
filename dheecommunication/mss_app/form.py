from statistics import mode
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.db.models import fields
from mss_app.models import *


class LoginForm(AuthenticationForm):
    def cleaned_username(self):
        user_name_got = self.cleaned_data.get('username')

        return user_name_got

class ClientProfileCreateForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = '__all__'


class CreditTranscationCreateForm(forms.ModelForm):
    class Meta:
        model = CreditTransaction
        fields = '__all__'


class DebitTranscationCreateForm(forms.ModelForm):
    class Meta:
        model = DebitTransaction
        fields = '__all__'

class MCashTranscationCreateForm(forms.ModelForm):
    class Meta:
        model = MCashTranscations
        fields = '__all__'


class AutoRefillTransactionForm(forms.ModelForm):
    class Meta:
        model = AutoRefillTransaction
        fields = '__all__'