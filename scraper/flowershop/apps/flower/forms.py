from django import forms
class Login(forms.Form):
    username = forms.CharField(label='Username', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)

class Registration(forms.Form):
    username = forms.CharField(label='Username', max_length=255)
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=255)
    confirm = forms.CharField(widget=forms.PasswordInput, label='Confim Password')