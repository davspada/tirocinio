from datetime import datetime
import os
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
    print("PROCESS {} STARTED ---- CAM : {}".format(os.getpid(), ip))
    
    #FPS = 1/TIMEOUT
    TIMEOUT = .1
    position = "lat 10 long 20"  #position placeholder
    old_timestamp = time.time()
    while(True):
    #for i in range(30):
        ret, frame = cap.read()
        timestamp = datetime.now()
        if (time.time() - old_timestamp) > TIMEOUT:
            frame = cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
            data_for_consumer = Frame_data(frame, timestamp, position, name)
            #cv2.imshow('frame',frame)
            queue.put(data_for_consumer)
            old_timestamp = time.time()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("CAMERA STOPPED")
                break
            if queue.qsize() > 5:
                break

    cap.release()
    cv2.destroyAllWindows()