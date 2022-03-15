#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Karthik Sivaraman
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  17/11/2021
#####################################################################


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User, Group
from tb_track_app.models import UserProfile, GroupProfile


class SignUpForm(UserCreationForm):
    user_id_field = forms.CharField(max_length=100)
    try:
        category_details = Group.objects.all()
        user_categories = [(i.id, i.name) for i in category_details]
        user_category = forms.ChoiceField(choices=user_categories)
    except:
        user_categories = []
        user_category = forms.ChoiceField(choices=user_categories)

    class Meta:
        model = User
        fields = (
        'username', 'password1', 'password2', 'user_id_field','user_category')

    def clean_user_id_field(self):
        useridfield_got = self.cleaned_data.get('user_id_field')

        if UserProfile.objects.filter(user_id_field=useridfield_got).exists():
            raise forms.ValidationError("User ID already exists !!!")

        return useridfield_got

    def clean_category(self):
        category_got = self.cleaned_data.get('user_category')
        return category_got


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid credentials. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


# class LoginForm(AuthenticationForm):
#     def cleaned_username(self):
#         user_name_got = self.cleaned_data.get('username')

#         return user_name_got



