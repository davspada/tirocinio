import cv2
import numpy as np

cap = cv2.VideoCapture('rtsp://admin:password@172.16.1.69//h264Preview_01_main')                   #reolink
#cap = cv2.VideoCapture('http://172.16.1.70:80/cgi-bin/encoder?USER=Admin&PWD=123456&GET_STREAM')   #ACTI ACM 8511P
#cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    #frame = cv2.flip(frame,1)
    width = int(cap.get(3))
    height = int(cap.get(4))
    frame = cv2.resize(frame,(0,0), fx=0.5,fy=0.5)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()