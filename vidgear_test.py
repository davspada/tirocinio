# import required libraries
from datetime import datetime
import multiprocessing
import os
import time
from vidgear.gears import CamGear
import cv2

link1 = 'rtsp://admin:password@172.16.1.64'
link2 = 'rtsp://admin:password@172.16.1.69'
position = '1024235'
queue = multiprocessing.Queue()

class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name


def process_data(queue):
    print("CONSUMER {} STARTED".format(os.getpid()))
    while(True):
        if not queue.empty():
            data = queue.get()
            name = data.name
            ts = data.timestamp
            ts.strftime("%m/%d/%Y-%H:%M:%-S")
            #IP YEAR MONTH DAY HOUR
            print("frames/"+str(name)+"/"+str(ts)+".jpg")
            cv2.imwrite("frames/"+str(name)+"/"+str(ts)+".jpg", data.frame)

def fun(queue,link,name):

    stream = CamGear(source= link ,logging=True).start()

    # loop over
    while True:

        # read frames from stream
        frame = stream.read()


        # check for frame if Nonetype
        if frame is None:
            print("no frame")
            break


        # {do something with the frame here}
        #frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
        timestamp = datetime.now()
        data_for_consumer = Frame_data(frame, timestamp, position, name)
        queue.put(data_for_consumer)

        #cv2.imshow("Output", frame)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # close output window
    cv2.destroyAllWindows()

    # safely close video stream
    stream.stop()


cons1 = multiprocessing.Process(target=fun,args=(queue,link1,1 ))
cons2 = multiprocessing.Process(target=fun,args=(queue,link2,2 ))

cons3 = multiprocessing.Process(target=process_data,args=(queue, ))
cons4 = multiprocessing.Process(target=process_data,args=(queue, ))

cons1.start()
cons2.start()
cons3.start()
cons4.start()
