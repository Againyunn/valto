from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Userinfo


YEARS= [x for x in range(1940,2022)]

class UserForm(UserCreationForm):
    # email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username",)#, "email")
        # labels = {
        #     'email' : '이메일'
        # }

class UserinfoForm(forms.ModelForm):
    birth = forms.DateField(label='생년월일을 입력하세요.', initial="2021-11-16", widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Userinfo
        fields = ["gender", "birth", "email"]
        labels = {
            'gender' : '성별',
            'birth' : '생년월일',
            'email' : 'email'
        }

