from django import forms

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
