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

def thread_func(cap,queue1, queue2, name, timestamp, position):
    _ , frame = cap.retrieve()
    frame = cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
    data_for_consumer = Frame_data(frame, timestamp, position, name)
    #cv2.imshow(name,frame)
    queue1.put(data_for_consumer)

#gets stream link, starts the capture, adds metadata to each frame and sends it to the queue
def camera_process_func(queue, ip, port, user, password, name):
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    cap = cv2.VideoCapture(str(cam_link))
    print("PROCESS {} STARTED ---- CAM : {}".format(os.getpid(), ip))
    #queue2 = multiprocessing.Queue()
    #FPS = 1/TIMEOUT
    TIMEOUT = .1
    position = "lat 10 long 20"  #position placeholder
    old_timestamp = time.time()
    while(True):
        ret = cap.grab()
        timestamp = datetime.now()
        timestamp2 = time.time()
        #print(timestamp2 - old_timestamp)
        if ((time.time() - old_timestamp) > TIMEOUT) and ret == True:
            #th = Process(target=thread_func,args=(cap,queue, queue2, name, timestamp, position))
            #th.start()
            _ , frame = cap.retrieve()
            frame = cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
            data_for_consumer = Frame_data(frame, timestamp, position, name)
            #cv2.imshow(name,frame)
            queue.put(data_for_consumer)
            old_timestamp = time.time()
            print(time.time() - old_timestamp)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("CAMERA STOPPED")
                break

    cap.release()
    cv2.destroyAllWindows()