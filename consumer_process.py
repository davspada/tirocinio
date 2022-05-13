from datetime import date
import os
from time import strftime
import cv2

def process_data(queue):
    #debug
    print("CONSUMER {} STARTED".format(os.getpid()))
    
    
    while(True):
        if not queue.empty():
            data = queue.get()
            
            #resizes frame
            rframe = cv2.resize(data.frame, (0, 0), fx=0.25, fy=0.25) 
            name = data.name
            ts = data.timestamp
            ts.strftime("%m/%d/%Y-%H:%M:%-S")
            #IP YEAR MONTH DAY HOUR 
            cv2.imwrite("frames/"+str(name)+"/"+str(ts)+".jpg", rframe)


#check se folder esiste  ---> si ---> piazza
#                        ---> no ---> crea ---> piazza

#creo prima la stringa a partire dal timestamp + nome della cam
#   ---> la uso per controllare il path se esiste o no
#   ---> eventualmente la uso anche per il imwrite