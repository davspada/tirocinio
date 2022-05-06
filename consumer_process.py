import os
import cv2

def process_data(queue):
    print("CONSUMER {} STARTED".format(os.getpid()))
    while(True):
        if not queue.empty():
            data = queue.get()
            ts = data.timestamp
            cv2.imwrite('frames/'+str(ts)+'.jpg', data.frame)
            print("file written --- "+str(ts))