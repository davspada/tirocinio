import datetime
import json
import os
import cv2
import requests
import ffmpeg

class Post_data:
  def __init__(self,path, frame, timestamp, position, name):
    self.path = path
    self.frame = frame
    self.timestamp = timestamp
    self.position = position
    self.name = name

url = 'http://172.16.1.72:8000/camera/get_camera_frames'

#files = {'frame': open('cameraApi/photo.jpg', 'rb')}
values = {"path" : "soldati/soldato/13456abcde","timestamp":"2022-05-23 13:24:23", "position":"position10", "name" : "camera1"}
auth=('davide','password')
data3 = '2022-05-26T13:26:21.574020Z'
#data1='2022/05/30 12:34:00'
#data2='2022/05/30 12:34:29'
data1='2022-06-27 11:47:30'
data2='2022-06-27 18:48:30'

reqvalues = {'name' :'00051539673100'}
#r = requests.post(url, files=files, data=values, auth=auth)
r= requests.get(url,data={'name' :'00051539673100','ts1': data1,'ts2': data2}, auth=auth)
#r = requests.delete(url,data={'name' :'00051539673100','ts1': data1,'ts2': data2}, auth=auth) 
#r = requests.delete(url, auth=auth)
#r = requests.get(url, auth=auth)
print(r.status_code)
#print(r.content)

lista = json.loads(r.content)
f = open('paths.txt', 'w+')
for i in lista:
  path = i['path']
  frame = i['frame']
  fullpath = path+frame
  print(fullpath)
  #f.write(fullpath+'\n')
  f.write("file '"+fullpath+"' \n")
f.close()

#ffmpeg.input('output.txt', r='20', f='concat', safe='0').output('video.mp4', vcodec='libx264').run()


"""
for single frame use
jsondata = r.json()
print(jsondata)
lista = json.loads(jsondata)
for j in lista:
    for i in j:
      pdata = Post_data(i["path"], i["frame"], i["timestamp"],i["position"],i["name"])
      path = pdata.frame
      #print(path)
      img = cv2.imread(path[1:], 1)
      cv2.imshow('frame', img)
      cv2.waitKey(0)
      #cv2.destroyAllWindows()
      cv2.destroyWindow('frame')
"""