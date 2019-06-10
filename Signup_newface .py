import face_recognition as fc
import numpy as np
import cv2
import time
import csv
import pandas as pd

v=cv2.VideoCapture(0)
fd=cv2.CascadeClassifier(r'C:\Users\dheer\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')


name=input("enter name")
def cap():
    flag=1
    while(flag):
        ret,i1=v.read()
        j=cv2.cvtColor(i1,cv2.COLOR_BGR2GRAY)#for gray color detection
        f=fd.detectMultiScale(j)
  
        if len(f)==1:
            for x,y,w,h in f:
                images=i1[y:y+h,x:x+w]#crop image
                flag=0
      
                cv2.imshow('dhsds',images)
                
               
                
                

    return images
i_1=cap()
img_nam=name+".jpg"
cv2.imwrite(img_nam,i_1)


'''Till now I used cv2 toread an image than crop it for my face and show it and tahn save it by my name'''

mob_no=int(input("enter mobile no."))
email_id=input("enter email id")
guardian_id=input("enter guardian email id")
mob_no_1=str(mob_no)


    
df=pd.read_csv('details_3.csv')
print(df)
a=0#crete intial attendance 
#mmake data frame with columns
df_1 = pd.DataFrame({'mobile_no':mob_no_1,
                  'name': [name],
                    'emailid': [email_id],
                   'guardian_email_id':[guardian_id],
                    'attendance':a})

#append it with previous dataset
datafram=df.append(df_1, ignore_index=True)
#save it in dataset
datafram.to_csv('details_3.csv',index=False)

