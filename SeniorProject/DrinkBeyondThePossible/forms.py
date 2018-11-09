from django import forms
from django.forms import ModelForm
from .models import customDrink, Comment, Tag

#class EditAccountForm(forms.Form):
#    account_name = forms.CharField(label='User Name', max_length=100)
#    password = forms.CharField(label='Password', max_length=100)

class EditAccountnameForm(forms.Form):
    account_name = forms.CharField(label='User Name', max_length=100)

class EditEmailForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)

class EditPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class NewAccountForm(forms.Form):
    account_name = forms.CharField(label='User Name', max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=100)

class NewDrinkForm(ModelForm):
    class Meta:
        model = customDrink
        fields = ['drink', 'ingredients', 'description', 'image', 'user']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class NewTagsForm(forms.Form):
    tags = forms.CharField(label='Tags', max_length=200)

