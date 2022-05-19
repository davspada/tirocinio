from datetime import datetime
import os
from time import strftime

import cv2

cap = cv2.VideoCapture(0) 
rframe, ret = cap.read() 
ts = datetime.now()

ts.strftime("%m/%d/%Y-%H:%M:%-S")
# IP YEAR MONTH DAY HOUR
fname = 'camera12345'
fyear = ts.strftime("%Y")
#print("year:", year)
fmonth = ts.strftime("%m")
#print("month:", month)
fday = ts.strftime("%d")
#print("day:", day)
fhour = ts.strftime("%H")
#print("hour:", hour)
fminute = ts.strftime("%M")
#print("minute:", minute)
fsecond = ts.strftime("%S")
#print("second:", second)

pathstring = 'frames/{name}/{year}/{month}/{day}/{hour}/{minute}/{second}/'.format(
    name=fname, year=fyear, month=fmonth, day=fday, hour=fhour, minute=fminute, second=fsecond)
#p = Path(pathstring)
# print(p)
os.makedirs(pathstring)

cv2.imwrite(pathstring+str(ts)+".jpg", rframe)
