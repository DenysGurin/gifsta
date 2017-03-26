from django import forms
from django.contrib.auth.models import User
from .models import Gif


class LoginForm(forms.Form):
	class Meta:
		model = User
		fields = ['username', 'password', ]

class RegisterForm(forms.ModelForm):
	confirm = forms.CharField(max_length=100)
	email = forms.EmailField(required=False)
	class Meta:
		model = User
		fields = ['username', 'password', 'confirm', 'email', ]

class PoolForm(forms.Form):
	pass

class UploadForm(forms.ModelForm):
	class Meta:
		model = Gif
		fields = ['name', 'tags', 'gif_file', ]
