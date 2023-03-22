from tkinter import Widget
from django import forms

from case.models import RegisterCase

class SearchCaseForm(forms.Form):
    Name = forms.CharField()
    Color = forms.CharField()
    Age = forms.IntegerField()
    Height = forms.FloatField()
    BodySize = forms.CharField()
    Mobile = forms.IntegerField()
    CloathingColor = forms.CharField()
    FrontView = forms.ImageField()
    LView = forms.ImageField()
    RView = forms.ImageField()



GENDER_CHOICE = [
        ("1", "Male"),
        ("2", "Female"),
        ("3", "Other")
    ]
class RegisterForm(forms.Form):
    # class Meta:
    #     model = RegisterCase 
    #     fields = ['Name','Address','Age','Gender','Height','BirthMark','BodySize','Date','Mobile','BodyColor','ClothingColor','FrontView','LView','RView']
    #     widgets = {
    #         'Date':
    #     }
    Name = forms.CharField()
    Address = forms.CharField()
    Age = forms.IntegerField()
    Gender = forms.ChoiceField(choices=GENDER_CHOICE)
    Height = forms.IntegerField()
    BirthMark = forms.CharField()
    BodySize = forms.CharField()
    Date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    Mobile = forms.IntegerField()
    BodyColor = forms.CharField(label='Body Color ')
    ClothingColor = forms.CharField(label="Cloths Color")
    FrontView = forms.ImageField(label="Front View")
    LView = forms.ImageField(label="Left Side View")
    RView = forms.ImageField(label="Right Side View")
