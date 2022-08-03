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
                print('Connected to gps socket')
                while(True):
                    data = s.recv(1024).decode("utf-8")
                    splitted_data = data.split('\r\n',2)
                    splitted_GLL = splitted_data[2]#.split(',')

                    msg = pynmea2.parse(splitted_GLL)
                    #self.position = msg.lat+msg.lat_dir+msg.lon+msg.lon_dir
                    subject.set_position(msg.lat+msg.lat_dir+msg.lon+msg.lon_dir)
                    #print(subject.get_position())
            except socket.error as e:
                print(e)
            finally:
                s.close()


if __name__ == '__main__':
    gps = GPSSubject()
    th = Thread(target=get_gps_data,args=(gps,))
    if(th.start()):
        print("thread started")
    else:
        print("thread not started")


"""
#MI INTERESSA GLLL --- prima lat poi long

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    data = s.recv(1024)
print(f"Received {data!r}")

SUBJECT = GPSSubject()
OBSERVER = GPSReceiver(SUBJECT)
#SUBJECT.get_gps_data()

#glll posizionale
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024).decode("utf-8")
    splitted_data = data.split('\r\n',2)
    splitted_GLL = splitted_data[2]#.split(',')

    msg = pynmea2.parse(splitted_GLL)
    position = msg.lat+msg.lat_dir+msg.lon+msg.lon_dir
    print(position)

    for data in splitted_data:
        data = data.replace('\r\n','')
        try:
            msg = pynmea2.parse(data,check=False)
            print(msg)
        except pynmea2.ParseError as e:
            print(e)



    #print(splitted_GLL)
    lat1 = splitted_GLL[1][0]+splitted_GLL[1][1]
    lat2 = splitted_GLL[1][2]+splitted_GLL[1][3]
    lat3 = splitted_GLL[1][4:9]
    lat_dir = splitted_GLL[2]
    long1 = splitted_GLL[3][0]+splitted_GLL[3][1] +splitted_GLL[3][2]
    long2 = splitted_GLL[3][3]+splitted_GLL[3][4]
    long3 = splitted_GLL[3][5:10]
    long_dir = splitted_GLL[4]
    position = lat1+"."+lat2+lat3+lat_dir+" "+long1+"."+long2+long3+long_dir
"""