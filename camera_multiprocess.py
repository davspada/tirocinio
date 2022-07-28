from datetime import datetime
import os
from threading import Thread
import time
import cv2
from requests import options
import camera_operations
from vidgear.gears import CamGear
from gps import GPSReceiver, GPSSubject, get_gps_data

#data package for consumer
class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name





#gets stream link, starts the capture, adds metadata to each frame and sends it to the queue
def camera_process_func(queue, ip, port, user, password, Gps : GPSSubject):
    
    #gets camera stream link
    cam_link, name = camera_operations.getStreamLink(ip, port, user, password)
    

    options = {"CAP_PROP_FRAME_WIDTH":320.0, "CAP_PROP_FRAME_HEIGHT":240.0}
    #camera istance
    stream = CamGear(source=cam_link, logging=True, **options).start() #
    print("PROCESS {} STARTED ---- CAM : {}".format(os.getpid(), ip))
    
    th = Thread(target=get_gps_data,args=(Gps,))
    th.start()

    #FPS = 1/TIMEOUT
    TIMEOUT = 0.5
    
    old_timestamp = time.time()
    #LOOP FOR STREAM
    while(True):
        #reads the frame      
        frame = stream.read()
        #gets the timestamp
        timestamp = datetime.now()
        #gets the position
        position = Gps.get_position()

        #chooses if the frame is to be kept or skipped
        if( time.time() - old_timestamp) > TIMEOUT:

          #do something with the frame
          #frame = cv2.resize(frame,(0,0), fx=0.25,fy=0.25)
          #cv2.imshow(name,frame)
          
          #creates the data package for the consumer
          data_for_consumer = Frame_data(frame, timestamp, position, name)
          
          #puts data in queue for consumer
          queue.put(data_for_consumer)
          
          #debug for performance
          #print(time.time()-old_timestamp)
          
          old_timestamp = time.time()
        
        #to stop showing cam if imshow()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("CAMERA STOPPED")
            th._stop()
            break

    stream.stop()
    cv2.destroyAllWindows()