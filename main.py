import multiprocessing
import camera_multiprocess, consumer_process
from camera_operations import populate_camera_list

processes_list = []
queue_mp = multiprocessing.Queue()
camera_list = []

populate_camera_list(camera_list)

for camera in camera_list:
    #print("trying to access ---"+camera.ip+ camera.port+ camera.user+camera.passw)
    proc = multiprocessing.Process(target = camera_multiprocess.camera_process_func,args=(queue_mp, camera.ip, camera.port, camera.user, camera.passw))
    processes_list.append(proc)

for i in range(2):
    cons = multiprocessing.Process(target=consumer_process.process_data,args=(queue_mp, ))
    processes_list.append(cons)


for proc in processes_list:
    proc.start()