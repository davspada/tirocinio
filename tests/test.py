from datetime import datetime
import time
import cv2
import numpy as np

class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name

name = '17216169'

cap = cv2.VideoCapture('rtsp://admin:password@172.16.1.69')                   #reolink
while(True):
    TIMEOUT = .1
    position = "lat 10 long 20"  #position placeholder
    old_timestamp = time.time()
    while(True):
        ret, frame = cap.read()
        timestamp = datetime.now()
        if (time.time() - old_timestamp) > TIMEOUT:
            frame = cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
            data_for_consumer = Frame_data(frame, timestamp, position, name)
            #cv2.imshow(name,frame)
            old_timestamp = time.time()
            name = data_for_consumer.name
            ts = data_for_consumer.timestamp
            ts.strftime("%m/%d/%Y-%H:%M:%-S")
            #IP YEAR MONTH DAY HOUR 
            cv2.imwrite("frames/"+str(name)+"/"+str(ts)+".jpg", data_for_consumer.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("CAMERA STOPPED")
                break

    cap.release()
    cv2.destroyAllWindows()