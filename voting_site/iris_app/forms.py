from django import forms
from .models import *


class Login_Form(forms.Form):
    Voter_id = forms.CharField(max_length=100)
    Phone_Number = forms.IntegerField()


class Votes_Form(forms.Form):
    Nominee_Id = forms.CharField(max_length=100)
    Nominee_Name = forms.CharField(max_length=100)
    Nominee_Photo = forms.ImageField()
    Party = forms.CharField(max_length=100)
    Sign = forms.ImageField()

    class meta:
        model = Votes
        fields = "__all__"


class photo_forms(forms.ModelForm):
    class Meta:
        model = Iris_model
        fields = ['iris_image']
