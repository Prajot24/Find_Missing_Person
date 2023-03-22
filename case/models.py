from distutils.command.upload import upload
from pyexpat import model
from django.contrib.auth.models import User
from turtle import up
from django.db import models
from django.forms import CharField, ImageField
import os 
from uuid import uuid4

# Create your models here.
def path_and_rename(instance, filename):
    print(filename, instance)
    print("*********************************************")
    upload_to = 'img'
    ext = filename.split('.')[-1]
    # get filename
    if instance:
        filename = '{}.{}'.format(instance.Name, ext)
    else:
        # set filename as random string 
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class RegisterCase(models.Model):
    Name = models.CharField(max_length=100)
    NickName = models.CharField(max_length=100,null=True)
    Address = models.CharField(max_length=300)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Height = models.FloatField()
    Weight = models.FloatField()
    DOB = models.DateField()
    BirthMark = models.CharField( max_length=100)
    DOM = models.DateField()
    Mobile = models.IntegerField()
    ClothingColor = models.CharField(max_length=50)
    Image = models.ImageField(upload_to=path_and_rename)
    Dis = models.CharField(max_length=100)
    MissingPlace = models.CharField(max_length=100)
    Status = models.BooleanField(default=False)
    User_ref = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class SearchCase(models.Model):
    Name = models.CharField(max_length=100,null=True)
    Color = models.CharField(max_length=50,null=True)
    Age = models.IntegerField(null=True)
    Height = models.FloatField(null=True)
    BodySize = models.CharField(max_length=10,null=True)
    Mobile = models.IntegerField(null=True)
    CloathingColor = models.CharField(max_length=50,null=True)
    FrontView = models.ImageField(upload_to=path_and_rename)
    LView = models.ImageField(upload_to=path_and_rename)
    RView = models.ImageField(upload_to=path_and_rename)


# class SearchImage(models.Model):
#     Image = models.ImageField(upload_to='img')
#     Person = models.ForeignKey(SearchCase,on_delete=models.CASCADE)

