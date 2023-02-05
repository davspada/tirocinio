from datetime import date
import multiprocessing
import os
from time import sleep, strftime
import cv2
from pathlib import Path
import psycopg2
import requests

#connection to db
conn = psycopg2.connect("dbname=framesdb user=dbuser host=localhost password=password")
cur = conn.cursor()

#username e password NON PIU' NECESSARI
class Post_data:
  def __init__(self, filename,pathstring, timestamp, position, name):
    self.filename = filename
    self.pathstring = pathstring
    self.timestamp = timestamp
    self.position = position
    self.name = name


#inserts data into database
def post_request(queue):
    
    while(True):
        if not queue.empty():
            #uncomment the following line to check how far behind the queue gets
            #print("POST Q: "+str(queue.qsize()))
            data =queue.get()
            query = f"INSERT INTO camera_api_data (frame, position, timestamp, name, path) VALUES ('{data.filename}', '{data.position}', '{data.timestamp}', '{data.name}', '{data.pathstring}')"
            cur.execute(query)
            conn.commit()


def process_data(queue, queue_post):
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            #uncomment the following line to check how far behind the queue gets
            #print("FRAME Q: "+str(queue.qsize()))
            data = queue.get()
            
            position = data.position
            #resizes frame
            rframe = cv2.resize(data.frame, (0, 0), fx=0.25, fy=0.25) 
            fname = data.name
            ts = data.timestamp
            ts.strftime("%m/%d/%Y%H:%M:%S")

            fyear = ts.strftime("%Y")
            fmonth = ts.strftime("%m")
            fday = ts.strftime("%d")
            fhour = ts.strftime("%H")
            fminute = ts.strftime("%M")
            fsecond = ts.strftime("%S")

            #local is for saving frames on local machine(frame is in machine and its location in the database)
            pathstring_local = 'cameraApi/media/images/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)
            #frame path should be formatted like this for the web interface to work properly
            pathstring_db = '/images/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)

            #creates folders if needed
            os.makedirs(pathstring_local,exist_ok=True)
            #creates filename
            filename = str(ts)+".jpg"
            #adds path to filename, for saving with opencv imwrite()
            filenameandpath = pathstring_local+str(ts)+".jpg"
            cv2.imwrite(filenameandpath, rframe)

            #puts data package in queue for storing in database
            post_data = Post_data(filename, pathstring_db, ts, position, fname)
            queue_post.put(post_data)
            

#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> la uso anche per il imwrite