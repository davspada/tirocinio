from collections import namedtuple
import json
from unicodedata import name
from numpy import size
from onvif import ONVIFCamera

class Camera:
  def __init__(self, ip, port, user, passw):
    self.ip = ip
    self.port = port
    self.user = user
    self.passw = passw

#gets camera list from json and populates a list for the program
def populate_camera_list(cam_list):
    with open('cameras.json') as json_file:
        data = json.load(json_file)
        for i in data['cameras']:
            cam = Camera(i["ip"], i["port"], i["user"],i["passw"])
            cam_list.append(cam)

#necessary for the link creation, as the program uses it
def appendCredencials(username, password, ip):
    return 'rtsp://'+username+':'+password+'@'+ip

#connects to camera via Onvif
def connectCamera(ip, port, user, passw):
    cam = ONVIFCamera(ip,port, user, passw)
    resp = cam.devicemgmt.GetDeviceInformation()
    #for debug
    #print('Connected to cam : ' +ip+' - Hostname : '+str(resp['SerialNumber']))
    name = str(resp['SerialNumber'])
    return cam, name

#gets stream link via onvif, the params for the GetStreamUri and mediaservice Profiles can be changed base on camera settings
def getStreamLink(ip, port, user, passw):
    cam, name = connectCamera(ip, port, user, passw)
    mediaService = cam.create_media_service()
    media_profiles = mediaService.GetProfiles()
    #print(media_profiles)
    token = media_profiles[0].token
    #if the uri is needed to create the stream link
    uri = mediaService.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'UDP'},'ProfileToken':token})
    print(uri)
    final_uri = appendCredencials(user,passw,ip)
    #print('Stream link : '+final_uri)
    return final_uri, name

#for testing purposes
if __name__ == '__main__':
    camera_list = []
    populate_camera_list(camera_list)
    for c in camera_list:
        getStreamLink(c.ip,c.port,c.user,c.passw)
