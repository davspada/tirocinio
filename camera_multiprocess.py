from datetime import datetime
import multiprocessing
from multiprocessing.dummy import Process
import os
from threading import Thread
import time
import cv2
import camera_operations


class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name

#gets stream link, starts the capture, adds metadata to each frame and sends it to the queue
def camera_process_func(queue, ip, port, user, password, name):
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    cap = cv2.VideoCapture(str(cam_link))

    cap.set(3,1280) # just to increase capture time
    cap.set(4,720) # just to increase capture time

    print("PROCESS {} STARTED ---- CAM : {}".format(os.getpid(), ip))
    print("FPS ----- "+str(cap.get(cv2.CAP_PROP_FPS)))
    #queue2 = multiprocessing.Queue()
   
   
    #FPS = 1/TIMEOUT
    TIMEOUT = 0
    position = "lat 10 long 20"  #position placeholder
    old_timestamp = time.time()
    #while(True):
    for i in range(50):
        ret = cap.grab()
        timestamp = datetime.now()
        if ((time.time() - old_timestamp) > TIMEOUT) and ret == True:
            _ , frame = cap.retrieve()
            data_for_consumer = Frame_data(frame, timestamp, position, name)
            queue.put(data_for_consumer)
            old_timestamp = time.time()
            #print(time.time() - old_timestamp)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("CAMERA STOPPED")
                break

    cap.release()
    cv2.destroyAllWindows()