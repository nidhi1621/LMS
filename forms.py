from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class NewUserForm(UserCreationForm):
	UserName = forms.CharField(max_length=50)

	class Meta:
		model = User
		fields = ("UserName", "password")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.username = self.cleaned_data['UserName']
		if commit:
			user.save()
		return user
        
class signup(forms.Form):
    Name = forms.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    confirmpassword = models.CharField(max_length=50)

class login(forms.Form):
    UserName = forms.CharField(max_length=50)
    password = forms.IntegerField()
    confirmpassword = models.CharField(max_length=30)

class Form(forms.Form):
    book_id = forms.IntegerField(help_text = "Enter the numeric value")
    book_name = forms.CharField(max_length=50)
    Author_Name = forms.CharField(max_length=50)
    Issue_date = forms.DateField(widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    # Book_Status = forms.BooleanField()
    
class view(forms.Form):
    book_id = forms.IntegerField(help_text = "Enter the numeric value")
    book_name = forms.CharField(max_length=50)
    Author_Name = forms.CharField(max_length=50)

class Issue(models.Model):
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=50)
    student_id = models.IntegerField()
    student_Name = models.CharField(max_length=50)
    Issue_date = models.DateField()

class returnbook(forms.Form):
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=50)
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=50, default='')
    issue_date = models.DateField()
    return_date = models.DateField()

class UpdateForm(forms.Form):
    book_id = forms.IntegerField(help_text = "Enter the numeric value")
    book_name = forms.CharField(max_length=50)


