from django import forms

from TeacherRegistration.models import Teacher
from StudentRegistration.models import Student
from .models import Admin
from datetime import date
from django.http import JsonResponse, response
from dateutil import parser
import datetime
import re

class TeacherLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class TeacherForm(forms.ModelForm):
    


    class Meta:
        model = Teacher
        fields = ['name', 'email','subject' ]
 
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please Enter Your Email Id")
            
        return email
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("please enter your name")
        return name
        

        
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise forms.ValidationError("Please Select subject")
        return subject
        
class AdminLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class AdminSignupForm(forms.ModelForm):

    class Meta:
        model = Admin
        fields = ['name', 'email' ]
 
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please Enter Your Email Id")
            
        return email
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("please enter your name")
        return name

class StudentLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()       

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'email']
 
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Please Enter Your Email Id")
            
        return email
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("please enter your name")
        return name    

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age:
            raise forms.ValidationError("please enter your age")
        return age   

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
           
class AdminUserForm(forms.Form):
    name = forms.CharField(max_length=100, label="Admin Name")
    email = forms.EmailField(label="Admin Email")