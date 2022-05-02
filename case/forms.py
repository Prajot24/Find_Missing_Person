from django import forms


GENDER_CHOICE = [
        ("1", "Male"),
        ("2", "Female"),
        ("3", "Other")
    ]
class RegisterForm(forms.Form):
    Name = forms.CharField()
    Address = forms.CharField()
    Age = forms.IntegerField()
    Gender = forms.ChoiceField(choices=GENDER_CHOICE)
    Height = forms.IntegerField()
    BirthMark = forms.CharField()
    BodySize = forms.CharField()
    Date = forms.DateField(widget=forms.DateInput)
    Mobile = forms.IntegerField()
    BodyColor = forms.CharField(label='Body Color ')
    ClothingColor = forms.CharField(label="Cloths Color")
    FrontView = forms.ImageField(label="Front View")
    LView = forms.ImageField(label="Left Side View")
    RView = forms.ImageField(label="Right Side View")
