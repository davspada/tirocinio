from datetime import date
import multiprocessing
import os
from time import sleep, strftime
import cv2
from pathlib import Path
import requests

url = 'http://172.16.1.76:8000/camera/post_frame'


class Post_data:
  def __init__(self, files, values, auth):
    self.files = files
    self.values = values
    self.auth = auth

def post_request(queue):
    
    while(True):
        if not queue.empty():
            print("POST Q: "+str(queue.qsize()))
            files, values, auth =queue.get()
            r = requests.post(url, files=files, data=values, auth=auth)

def process_data(queue, queue_post):
    #debug
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            print("FRAME Q: "+str(queue.qsize()))
            data = queue.get()
            
            #resizes frame
            rframe = cv2.resize(data.frame, (0, 0), fx=0.25, fy=0.25) 
            fname = data.name
            ts = data.timestamp
            ts.strftime("%m/%d/%Y-%H:%M:%-S")
            #IP YEAR MONTH DAY HOUR 

            fyear = ts.strftime("%Y")
            #print("year:", year)
            fmonth = ts.strftime("%m")
            #print("month:", month)
            fday = ts.strftime("%d")
            #print("day:", day)
            fhour = ts.strftime("%H")
            #print("hour:", hour)
            fminute = ts.strftime("%M")
            #print("minute:", minute)
            fsecond = ts.strftime("%S")
            #print("second:", second)

            pathstring = 'images/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)
            #p = Path(pathstring)
            #print(p)
            os.makedirs(pathstring,exist_ok=True)

            cv2.imwrite(pathstring+str(ts)+".jpg", rframe)
            #print("WROTE ------ "+str(pathstring)+str(ts)+".jpg")

            files = {'frame': open(str(pathstring)+str(ts)+".jpg", 'rb')}
            values = {"path" : pathstring ,"timestamp": ts, "position":"position10", "name" : fname}
            auth=('davide','password')

            post_data = Post_data(files, values, auth)

            queue_post.put(post_data)
            

            


#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> eventualmente la uso anche per il imwrite