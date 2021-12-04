from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import Student, User, Subject
# from grade_viewer import settings
from users.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        # model = Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                  'is_admin', 'is_teacher', 'is_student')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


REMARKS = (
    ('1', 'Passed'),
    ('2', 'Failed'),
    ('3', 'No Grade'),
    ('4', 'Incomplete')
)


class UpdateGradeForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['grade', 'remarks']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.Select(choices=REMARKS, attrs={'class': 'form-control'})
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class StudentInformationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class StudentSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
