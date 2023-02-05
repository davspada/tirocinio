import os
import socket
from threading import Thread
import pynmea2

HOST = '172.16.0.183'
PORT = 2222

class GPSSubject:

    def __init__(self, position = None):
        self.position = position

    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position

def get_gps_data(subject : GPSSubject):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                print('Connected to gps socket with process {}'.format(os.getpid()))
                while(True):
                    data = s.recv(1024).decode("utf-8")
                    splitted_data = data.split('\r\n',2)
                    splitted_GLL = splitted_data[2]#.split(',')

                    msg = pynmea2.parse(splitted_GLL)
                    subject.set_position(msg.lat+msg.lat_dir+msg.lon+msg.lon_dir)

            except socket.error as e:
                print(e)
            finally:
                s.close()

#for testing purposes
if __name__ == '__main__':
    gps = GPSSubject()
    th = Thread(target=get_gps_data,args=(gps,))
    if(th.start()):
        print("thread started")
    else:
        print("thread not started")