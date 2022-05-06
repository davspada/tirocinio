import multiprocessing
import camera_multiprocess
from camera_operations import populate_camera_list

processes_list = []
queue = multiprocessing.Queue()
camera_list = []

populate_camera_list(camera_list)

for camera in camera_list:
    print("trying to access ---"+camera.ip+ camera.port+ camera.user+camera.passw)
    proc = multiprocessing.Process(target = camera_multiprocess.camera_process_func,args=(queue, camera.ip, camera.port, camera.user, camera.passw))
    processes_list.append(proc)

for proc in processes_list:
    proc.start()