from datetime import date
import multiprocessing
import os
from time import sleep, strftime
import cv2
from pathlib import Path
import requests

url = 'http://172.16.1.55:8000/camera/post_frame'
username = 'davide'
password = 'password'

class Post_data:
  def __init__(self, filename,pathstring, timestamp, position, username, password, name):
    self.filename = filename
    self.pathstring = pathstring
    self.timestamp = timestamp
    self.username = username
    self.password = password
    self.position = position
    self.name = name

def post_request(queue):
    
    while(True):
        if not queue.empty():
            print("POST Q: "+str(queue.qsize()))
            data =queue.get()
            files = {'frame': open(data.filename, 'rb')}
            values = {"path" : data.pathstring ,"timestamp": data.timestamp, "position":data.position, "name" : data.name}
            r = requests.post(url, files=files, data=values, auth=('davide','password'))
            print(r._content)

def process_data(queue, queue_post):
    #debug
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            #print("FRAME Q: "+str(queue.qsize()))
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
            filename = pathstring+str(ts)+".jpg"
            cv2.imwrite(filename, rframe)
            #print("WROTE ------ "+str(pathstring)+str(ts)+".jpg")

            #files = {'frame': open(str(pathstring)+str(ts)+".jpg", 'rb')}
            #values = {"path" : pathstring ,"timestamp": ts, "position":"position10", "name" : fname}
            #auth=('davide','password')

            post_data = Post_data(filename, pathstring, ts, "position11" , fname, username, password)

            queue_post.put(post_data)
            

            


#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> eventualmente la uso anche per il imwrite