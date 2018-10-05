from django import forms

class EditAccountForm(forms.Form):
    account_name = forms.CharField(label='User Name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class NewAccountForm(forms.Form):
    account_name = forms.CharField(label='User Name', max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=100)
