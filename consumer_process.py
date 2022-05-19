from datetime import date
import os
from time import sleep, strftime
import cv2
from pathlib import Path

def process_data(queue):
    #debug
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            #print(queue.qsize())
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

            pathstring = 'frames/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)
            #p = Path(pathstring)
            #print(p)
            os.makedirs(pathstring)

            #cv2.imwrite("frames/"+name+"/"+str(ts)+".jpg", rframe)
            cv2.imwrite(pathstring+str(ts)+".jpg", rframe)
        else:
            sleep(0.01)


#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> eventualmente la uso anche per il imwrite