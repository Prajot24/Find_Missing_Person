from ast import Add
import json
from ntpath import join
from pickletools import read_uint1
from unicodedata import name
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import cv2 
import numpy as np
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from case.forms import RegisterForm, SearchCaseForm
from case.models import RegisterCase,  SearchCase
from findperson import settings
import face_recognition
import urllib.request
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from elasticsearch import Elasticsearch
from . import core

es = core.create_connection();
# Create your views here.
def Signin(request):
    if request.method == "POST":
      user_inst = User.objects.get(username=request.POST['mobile'])
      user_name = user_inst.username
      password = user_inst.last_name
      user = authenticate(username=user_name,password=password)
      if user is not None:
        form = login(request,user)
        print("Login successfully!")
        return redirect('/dashboard/')
      else:
        return HttpResponse("Please Check Your login Details")  

    return render(request,'login.html')

def Signout(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == "POST":
        p_inst = request.POST
        name = p_inst['name']
        email =  p_inst['email']
        mobile =  p_inst['mobile']
        password =  p_inst['password']
        # Save User object here and 
        user = User.objects.create_user(mobile,email,password)
        user.first_name = name
        user.last_name = p_inst['password']
        user.save() 
        # user = authenticate(name,password)
        # if user is not None:
        form = login(request,user)
        return redirect('/dashboard/')
        
    return render(request,'UserRegister.html')







def register_case(request):
    if request.method == "POST":
        print(request.POST)
        
        # Get Person info here
        photo = request.FILES['Image']
        form = RegisterCase(
            Name=request.POST['Name'],
            NickName = request.POST['NickName'],
            Address=request.POST['Address'],
            Age=request.POST['Age'],
            Gender=request.POST['Gender'],
            BirthMark=request.POST['BirthMark'],
            Weight=request.POST['Weight'],
            Height=request.POST['Height'],
            DOM=request.POST['DOM'],
            DOB=request.POST['BOD'],
            Mobile=request.POST['Mobile'],
            ClothingColor=request.POST['LastCloths'],
            Image=request.FILES['Image'],
            Dis = request.POST['Dis'],
            MissingPlace = request.POST['MissingPlace'],
            User_ref = request.user
        )

        form.save()
        get_url = "http://127.0.0.1:8000"+form.Image.url
        req = urllib.request.urlopen(get_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img2= cv2.imdecode(arr, -1) # 'Load it as it is'
        rgb_image2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        ref_img = face_recognition.face_encodings(rgb_image2)[0]
        print(ref_img)
        core.add_embedding(es,ref_img,form.Name,form.id)

        get_case = RegisterCase.objects.all()
        for i in get_case:
            print(i.Image.url)
        return redirect("/dashboard")

    else:
        Registerform = RegisterForm()
    Registerform = RegisterForm()

    return render(request, 'register.html', {'form': Registerform})


def Search(request):
    if request.method == "POST":
        print(request.POST, request.FILES)
        # form = SearchCase(
        #     Name =request.POST['Name'],
        #     Color = request.POST['Color'],
        #     Age= request.POST['Age'],
        #     Height= request.POST['Height'],
        #     BodySize= request.POST['BodySize'],
        #     Mobile= request.POST['Mobile'],
        #     CloathingColor=request.POST['CloathingColor'],
        #     FrontView=request.FILES['FrontView'],
        #     LView=request.FILES['LView'],
        #     RView=request.FILES['RView']
        # )

        form.save()
        return redirect('/dashboard')
    else:
        form = SearchCaseForm()
    form = SearchCaseForm()
    return render(request, 'SearchPage.html')
    return HttpResponse('In Search Field')

def extractName(data):
    data = data.rsplit('.',1)[0]
    name = data.split("_")
    return name

def getFaceEncoding(url):
    get_url = "http://127.0.0.1:8000"+url
    req = urllib.request.urlopen(get_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img2= cv2.imdecode(arr, -1) # 'Load it as it is'
    rgb_image2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)


    return rgb_image2

def dashboard(request):
    if request.method == "POST":
        print(request.POST)
    print("Printing --------------------->",request.user.id)

    cases = RegisterCase.objects.filter(User_ref=request.user.id)

    return render(request,'dashboard.html',{'cases':cases})

def findperson(request):
    if request.method == "POST":
        name = "No data Found "
        file_name = ""
        get_image = request.FILES['inputImage']
        get_Name = request.POST['PersonName']
        print(get_Name)

        p = os.path.join(settings.MEDIA_ROOT, "somename.jpeg")
        print(p)
        file_exist = os.path.exists(p)
        if file_exist:
            os.remove(p) 
            print("File removed Successfully!")
            #delete that file 
        path = default_storage.save('somename.jpeg', ContentFile(get_image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        b_array = ""
        # print("Printing Array ",request.FILES["inputImage"].chunks())

        # for line in request.FILES["inputImage"]:
        #     print(line)
        #     b_array=b_array+str(line)
        # print("Printing Image ",b_array)
        # img = cv2.imdecode(np.fromstring(b_array,np.uint8),cv2.IMREAD_UNCHANGED)
        start = datetime.datetime.now()
        #Use for loop for all images 

        img = cv2.imread(p) # Array of image  
        rgb_image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # Color conversion BGR to RGB 
        img_encode = face_recognition.face_encodings(rgb_image)[0] # encode image 
        id = core.search_person_embedding(es=es,img_encode=img_encode)
        if id:
            persons_inst=RegisterCase.objects.get(id=id)
            get_url = persons_inst.Image.url
            get_url = "http://127.0.0.1:8000"+get_url
            end = datetime.datetime.now()
            duration = end - start
            return render(request,'SearchPerson.html',{'name':persons_inst.Name,'link':get_url,'person':persons_inst,'current':"somename.jpeg",'time':duration})

      
   
        # persons_list = RegisterCase.objects.filter(Name__icontains=get_Name)
        # print(persons_list.count,"printing count of queryset --------------------")
        # if persons_list.count == 0 :
        #     persons_list = RegisterCase.objects.all()

        # for persons_inst in persons_list:
        #     get_url = persons_inst.Image.url

        #     get_url = "http://127.0.0.1:8000"+get_url
        #     req = urllib.request.urlopen(get_url)
        #     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        #     img2= cv2.imdecode(arr, -1) # 'Load it as it is'
        #     rgb_image2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        #     ref_img = face_recognition.face_encodings(rgb_image2)[0]
        #     result = face_recognition.compare_faces([ref_img],img_encode)[0]
        #     if result:
        #         end = datetime.datetime.now()
        #         duration = end - start
        #         return render(request,'SearchPerson.html',{'name':persons_inst.Name,'link':get_url,'person':persons_inst,'current':"somename.jpeg",'time':duration})

        # Here is working code
        # get_file_names = os.path.join(settings.MEDIA_ROOT,'img')

        # print(get_file_names)
        # img = {}
        # files = os.listdir(get_file_names)
        # img_array = []
        # for f in files:
        #     print(f)
        #     get_path_img = os.path.join(get_file_names,f)
        #     img2 = cv2.imread(get_path_img)
        #     rgb_image2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
        #     ref_img = face_recognition.face_encodings(rgb_image2)[0]
        #     result = face_recognition.compare_faces([ref_img],img_encode)[0]
        
        # This is end of working code 

            # img_array.append(ref_img)
            # img[f]="";
            # print(result)


        # THis is also part of working code 
            # if result:
            #     file_name = f
            #     name = ' '.join(extractName(f))
            #     break

        # end of working code 

            # img[get_path_img] = result
            # result = face_recognition.compare_faces([img_encode1,img_encode2], img_encode)

        # result = face_recognition.compare_faces(img_array,img_encode)
        # # matched = []
        # count = 0
        # d = chr(92)
        # for i in img:
        #     if result[count]:
        #         file_name = i
        #         name = ' '.join(extractName(i))
        #         # matched.append(get_file_names+d+i)
        #     count = count + 1

       
        # print(result)
        # print(matched)
    #working 
        # return render(request,'SearchPerson.html',{'name':name,'link':file_name,'person':person_obj,'current':"somename.jpeg"})

        # myfile = get_image.read()
        # print(myfile)
        # image = cv2.imdecode(numpy.frombuffer(myfile , numpy.uint8), cv2.IMREAD_UNCHANGED)
        # print(image)        
    return render(request,'SearchPerson.html',{'name':''})