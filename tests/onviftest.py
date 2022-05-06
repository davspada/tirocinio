from asyncio import streams
from urllib.request import HTTPDigestAuthHandler
from onvif import ONVIFCamera, ONVIFService
import cv2
import numpy as np
import requests
from requests.auth import HTTPDigestAuth

ip = '172.16.1.70'
port = '8000'
user = 'Admin'
passw = '123456'

cam = ONVIFCamera(ip,port, user, passw)
# Get Hostname
resp = cam.devicemgmt.GetHostname()
print('My camera`s hostname: ' + str(resp.Name))

mediaService = cam.create_media_service()
media_profiles = mediaService.GetProfiles()
token = media_profiles[0].token
uri = mediaService.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'UDP'},'ProfileToken':token})
prefactor_uri = uri['Uri']
print(prefactor_uri)

def appendCredencials(pre_uri, username, password):
    return 'rtsp://'+username+':'+password+'@'+ip

final_uri = appendCredencials(prefactor_uri,user,passw)
print(final_uri)
cap = cv2.VideoCapture(final_uri)
while(True):
#for i in range(30):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5) 
    #width = int(cap.get(3))
    #height = int(cap.get(4))
    cv2.imshow('frame',frame)
    #cv2.imwrite('frames/gr'+str(i)+'.jpg', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


#cap = cv2.VideoCapture('rtsp://admin:password@172.16.1.69//h264Preview_01_main')                   #reolink
#cap = cv2.VideoCapture('http://172.16.1.70:80/cgi-bin/encoder?USER=Admin&PWD=123456&GET_STREAM')   #ACTI ACM 8511P