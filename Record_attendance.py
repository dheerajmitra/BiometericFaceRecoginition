import face_recognition as fc
import numpy as np
import cv2
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from random import random
import pandas as pd

df=pd.read_csv('details_3.csv')

name=[]
name_email=[]
guard_email=[]
attend=[]
set_img=[]
# I take empty list so they can take all value of single column per list and also to load image
for i in range(len(df['name'])):
     name.append(df['name'][i])
     name_email.append(df['emailid'][i])
     guard_email.append(df['guardian_email_id'][i])
     attend.append(df['attendance'][i])
     a=df['name'][i]+".jpg"
     iw=fc.load_image_file(a)
     set_img.append(iw)

#make note of start time   
tim=time.localtime()
fcl=[]
for i in range(len(df['name'])):
   
    fl=fc.face_locations(set_img[i])
    print(fl)
    fcl.append(fc.face_encodings(set_img[i],fl))
    
#in above for loop convet image into 128 array size for face recoginition    
fd=cv2.CascadeClassifier(r'C:\Users\dheer\AppData\Local\Programs\Python\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
#create 2 object for email id such that one for user and one for guardian of user
msg = MIMEMultipart()
msg_1=MIMEMultipart()
# create an otp by random library
m_i=int(random()*10000)
message=str(m_i)
#owner email id and password
password = "testpython12"
msg['From'] = "testpythonsid@gmail.com"
#adding subject for each email
msg['Subject'] = "OTP Genrated"
msg_1['Subject'] = "Attendance detail"
        

# add in the message body
msg.attach(MIMEText(message, 'plain'))


#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)

 
flag=1
t=0
while(flag):
    v=cv2.VideoCapture(0)
    ret,i1=v.read()#live camera reading
    fm=fc.face_locations(i1)
    fml=fc.face_encodings(i1,fm)
    #encode live image encode into 128 values
    if len(fml)!=0:
        for i in range(len(df['name'])):
        
            f=fc.compare_faces(fcl[i],fml[0])#comparison between image
    
            print(f)
            
            #find the person belongs to image
            if f[0]==True:
                print("hi")
                index_no=i
                t=1
                break
        x1,y2,x2,y1 = fm[0]
        cv2.rectangle(i1,(x1,y1),(x2,y2),(0,0,255),3)
        #cv2.putText(i1, name[index_no], (x1,y1),2, (0,255,255),1) 
           
        cv2.imshow('te',i1)
    
                
            
        
        if t==1:
              flag=0
       
          
              if tim[3]==10  and tim[4]<=59:
                  print("hi "+name[index_no])#print name
                  server.sendmail(msg['From'], name_email[index_no], msg.as_string())   # send the otp via the server.
                  print("enter your otp")
                  start_tim=time.localtime()[4]
                  otp=int(input("enter otp"))
                  ov_time=time.localtime()[4]
                  if (ov_time-start_tim)>10: #checking time duration for which user can enter otp
                      print("session time run out again scan your face")
                  elif  otp!=m_i:# checking otp enter correct or not
                      print("otp entered is wrong")
                  else:
                      print("your attendance recorded succesfuly")
                      attend[index_no]+=1
                      message_1=" your ward is present today and attendance till up to date is "+str(attend[index_no])
                      #add attendance to database
                      df['attendance'][index_no]=attend[index_no]
                      df.to_csv('details_3.csv',index=False)
                      msg_1.attach(MIMEText(message_1, 'plain'))
                      server.sendmail(msg['From'], guard_email[index_no], msg_1.as_string())# send the message to guardian via the server.

              else:
                  print('Sorry you out of time')
                  
        else:
           flag=0
           print('face not matched')
           
          
                
                            
            
      
    
      
    
