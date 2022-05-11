from datetime import datetime
import threading
import time
import queue
import cv2
import camera_operations
import multiprocessing
import consumer_process


position = "lat 10 long 20"
frames = queue.Queue()
processes_list = []
camera_list = []

camera_operations.populate_camera_list(camera_list)


class Frame_data:
  def __init__(self, frame, timestamp, position, name):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name


class ImageGrabber(threading.Thread):
    def __init__(self, ID, link):
        threading.Thread.__init__(self)
        self.ID=ID
        self.cam=cv2.VideoCapture(str(link))
        self.cam.set(3,1280) # just to increase capture time
        self.cam.set(4,1024) # just to increase capture time
        self.runFlag=True

    def run(self):
        print("sub started")
        global frames
        while self.runFlag:
            ret,frame=self.cam.read()
            timestamp = datetime.now()
            data_for_consumer = Frame_data(frame, timestamp, position, name)
            frames.put(data_for_consumer)
            time.sleep(0.01)
        self.cam.release()


    def stop(self):
        self.runFlag=False




for camera in camera_list:
    #print("trying to access ---"+camera.ip+ camera.port+ camera.user+camera.passw)
    name = camera.ip.replace(".","")
    link = camera_operations.getStreamLink(camera.ip,camera.port,camera.user,camera.passw)
    proc = ImageGrabber(name, link)
    processes_list.append(proc)

for i in range(2):
    cons = multiprocessing.Process(target=consumer_process.process_data,args=(frames, ))
    processes_list.append(cons)

for proc in processes_list:
    proc.start()


