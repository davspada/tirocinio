from datetime import datetime
import os
import time
import cv2
from requests import options
import camera_operations
from vidgear.gears import CamGear


#data package for consumer
class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name





#gets stream link, starts the capture, adds metadata to each frame and sends it to the queue
def camera_process_func(queue, ip, port, user, password, name):
    
    #gets camera stream link
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    

    options = {"CAP_PROP_FRAME_WIDTH":320.0, "CAP_PROP_FRAME_HEIGHT":240.0}
    #camera istance
    stream = CamGear(source=cam_link, logging=True, **options).start() #
    print("PROCESS {} STARTED ---- CAM : {}".format(os.getpid(), ip))
    
    
    #FPS = 1/TIMEOUT
    TIMEOUT = 0
    position = "lat 10 long 20"  #position placeholder
    
    old_timestamp = time.time()
    #LOOP FOR STREAM
    while(True):

        frame = stream.read()
        timestamp = datetime.now()

        if( time.time() - old_timestamp) > TIMEOUT:
          #reads frame and adds timestamp

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
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("CAMERA STOPPED")
            break

    stream.stop()
    cv2.destroyAllWindows()