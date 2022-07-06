from datetime import date
import multiprocessing
import os
from time import sleep, strftime
import cv2
from pathlib import Path
import psycopg2
import requests

url = 'http://172.16.1.83:8000/camera/post_frame'
username = 'davide'
password = 'password'

#connection to db
conn = psycopg2.connect("dbname=framesdb user=dbuser host=localhost password=password")
cur = conn.cursor()

#username e password NON PIU' NECESSARI
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
            #print("POST Q: "+str(queue.qsize()))
            data =queue.get()
            query = f"INSERT INTO camera_api_data (frame, position, timestamp, name, path) VALUES ('{data.filename}', '{data.position}', '{data.timestamp}', '{data.name}', '{data.pathstring}')"
            cur.execute(query)
            conn.commit()
            #print("inserted ---", data.name, data.timestamp)


def process_data(queue, queue_post):
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            #print("FRAME Q: "+str(queue.qsize()))
            data = queue.get()
            
            position = data.position
            #resizes frame
            rframe = cv2.resize(data.frame, (0, 0), fx=0.25, fy=0.25) 
            fname = data.name
            ts = data.timestamp
            ts.strftime("%m/%d/%Y%H:%M:%S")

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

            pathstring = 'cameraApi/media/images/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)

            os.makedirs(pathstring,exist_ok=True)
            filename = str(ts)+".jpg"
            filenameandpath = pathstring+str(ts)+".jpg"
            cv2.imwrite(filenameandpath, rframe)


            post_data = Post_data(filename, pathstring, ts, position, username, password, fname)

            queue_post.put(post_data)
            

            


#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> eventualmente la uso anche per il imwrite