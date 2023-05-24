import sys
from django.shortcuts import render
from django.contrib import messages
import keras
from PIL import Image
from django.core.files.storage import default_storage
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyrebase
config={ 
  "apiKey": "AIzaSyCGo_C2UnProWBNL-gZ_GQ53p8v4tE-pMg",
  "authDomain": "smart-diagnosis-5e9c4.firebaseapp.com",
  "databaseURL": "https://smart-diagnosis-5e9c4-default-rtdb.firebaseio.com",
  "projectId": "smart-diagnosis-5e9c4",
  "storageBucket": "smart-diagnosis-5e9c4.appspot.com",
  "messagingSenderId": "133206915611",
  "appId": "1:133206915611:web:7395a05daede973b0516be",
  "measurementId": "G-27E4K8D6B4"

}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()

store=firebase.storage()
db=firebase.database()

def index(request):
        Name=request.POST.get('in_name')
        Email=request.POST.get('in_email')
        subject=request.POST.get('in_subject')
        meassge=request.POST.get('in_message')
        data_c = {
           
                            
             "email":Email,
            "namep": Name,
            "subject":subject,
            "Meassge":meassge,
            
        }                         
        db.child('Contact').push(data_c)


        return render(request,'index.html')

def Admin(request):
    #  email=request.POST.get('email_dr_ass')
    #  pasw=request.POST.get('pass_DR_ass')
    #  try:

    #     # if there is no error then signin the user with given email and password
    #     user=authe.sign_in_with_email_and_password(email,pasw)
    #  except:
    #     message="Invalid Credentials!!Please ChecK your Data"
    #     return render(request,"Admin.html",{"message":message})
    #  session_id=user['idToken']
    #  request.session['uid']=str(session_id)
     return render(request,'Admin.html')

def Doctor(request):
        
        iid = db.child('pat').child('id').get().val()
        namep = db.child('pat').child('name').get().val()
        age = db.child('pat').child('age').get().val()
        genbo = db.child('pat').child('genbox').get().val()
        imgurl = db.child('pat').child('url').get().val()

        return render(request,"Doctor.html",{"id":iid,"name":namep,"age":age ,"genbox":genbo,"url":imgurl})



# Create your views here.
media='media'
model = keras.models.load_model('Dr_92.h5')
predictions=["Mild","Moderate","NO_DR","Proliferate_DR","Severe"] 

def predict_new(path):
    img = cv2.imread(path)

    RGBImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    RGBImg= cv2.resize(RGBImg,(224,224))
    # plt.imshow(RGBImg)
    image = np.array(RGBImg) / 255.0
    predict=model.predict(np.array([image]))
    
    pred=np.argmax(predict,axis=1)
    return {predictions[pred[0]]}


def Dr_assint(request):
    if request.method == "POST" and request.FILES['upload']:
        
            
        if 'upload' not in request.FILES:
            err='No images Selected'
            return render(request,'Dr_assint.html',{'err':err})
        f = request.FILES['upload']
        if f== '':
            err='NO files selected'
            return render(request,'Dr_assint.html',{'err':err})
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file =default_storage.save(upload.name,upload)

        file_url=fss.url(file)
        id=request.POST.get('in_id')
        Name=request.POST.get('in_name')
        Age=request.POST.get('in_age')
        Gender=request.POST.get('in_gender')
        store.child(upload.name).put(upload)

        imgurl = store.child(upload.name).get_url(None)
        predictions=predict_new(os.path.join(media,file))
        # result=predictions

        data = {
           
                            
             "Id":id,
            "namep": Name,
            "age":Age,
            "genbox":Gender,
            
             "url":imgurl
            
        }                         
        db.child('pat').push(data)


        messages.success(request, "File upload in Firebase Storage successful")
        return render(request,'Dr_assint.html',{'pred':predictions,'file_url':file_url})
    
        
    else:
        
        return render(request,'Dr_assint.html')

def ta(request):
    return render(request,'ta.html')


