from django import forms 
from django.core import validators
from myapp.models import userInformation




class InputCity(forms.Form):
    city = forms.CharField(label="City", widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder': 'City', 
        'required': 'true'
        }))
    state = forms.CharField(label="State", widget=forms.TextInput(attrs={
        'class':'form-control', 
        'placeholder': 'State', 
        'required': 'true'}))

   



"""
-------------- ARCHIVE ---------------

# class FormName(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField()
#     verify_email = forms.EmailField(label="Please enter your email again.")
#     text = forms.CharField(widget=forms.Textarea)
#     botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

#     def clean(self):
#         all_clean_data = super().clean()
#         mail = all_clean_data['email']
#         vmail = all_clean_data['verify_email']

#         if mail != vmail:
#             raise forms.ValidationError("EMAILS DO NOT MATCH, PLEASE CHECK!")

"""