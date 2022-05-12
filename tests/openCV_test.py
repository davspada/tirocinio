from hashlib import new
from multiprocessing import Queue
import multiprocessing
import cv2
import numpy as np
import time
import consumer_process

class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name

queue = multiprocessing.Queue()

cons = multiprocessing.Process(target=consumer_process.process_data,args=(queue, ))

cap = cv2.VideoCapture('rtsp://admin:password@172.16.1.69')
print(cap.get(cv2.CAP_PROP_FPS))
cap.set(3,1280) # just to increase capture time
cap.set(4,1024) # just to increase capture time
timest = time.time()


while(True):
    ret, frame = cap.read()
    newtime = time.time()
    #frame = cv2.resize(frame,(0,0), fx=0.5,fy=0.5)
    #cv2.imshow('frame',frame)
    print( timest - newtime )
    timest = newtime
    data_for_consumer = Frame_data(frame, newtime, 'position', 'camera')
    queue.put(data_for_consumer)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()