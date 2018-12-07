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

class NewDrinkForm(forms.Form):
    drinkName = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200, required=False)
    instructions = forms.CharField(max_length=200, required=False)
    image = forms.FileField(required=False)

    class Meta:
        model = customDrink
        fields = ['drink', 'ingredients', 'description', 'image', 'user']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class EditCommentForm(forms.Form):
    c_id = forms.CharField(max_length=60,widget=forms.HiddenInput())
    message = forms.CharField(label='New Message', max_length=2000)

class NewTagsForm(forms.Form):
    tags = forms.CharField(label='Enter Tag(s) with commas:', max_length=200)

