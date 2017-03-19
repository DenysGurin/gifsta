from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	pass

class RegisterForm(forms.ModelForm):
	confirm = forms.CharField(max_length=100)
	email = forms.EmailField(required=False)
	class Meta:
		model = User
		fields = ['username', 'password', 'confirm', 'email', ]

class PoolForm(forms.Form):
	pass

class UploadForm(forms.Form):
	pass

