import multiprocessing
from threading import Thread
import camera_multiprocess, consumer_process
from camera_operations import populate_camera_list
from gps import GPSSubject

processes_list = []
queue_mp = multiprocessing.Queue()
queue_post = multiprocessing.Queue()
camera_list = []

populate_camera_list(camera_list)

#choose the number for the consumer processes
def choose_cons_number():
    print("inserire il numero di consumatori :")
    cons = int(input())
    return cons

#instance of the gps simulator
gpsubj = GPSSubject()

#creates a process for every camera
for camera in camera_list:
    #print("trying to access ---"+camera.ip+ camera.port+ camera.user+camera.passw)
    name = camera.ip.replace(".","")
    proc = multiprocessing.Process(target = camera_multiprocess.camera_process_func,args=(queue_mp, camera.ip, camera.port, camera.user, camera.passw, gpsubj))
    processes_list.append(proc)


cn = choose_cons_number()
for i in range(cn):
    cons = multiprocessing.Process(target=consumer_process.process_data,args=(queue_mp, queue_post))
    processes_list.append(cons)

post_cons = multiprocessing.Process(target=consumer_process.post_request,args=(queue_post, ))
processes_list.append(post_cons)

for proc in processes_list:
    proc.start()