import time
import cv2
import camera_operations


class Frame_data:
  def __init__(self, frame, timestamp, position):
    self.frame = frame
    self.timestamp = timestamp
    self.position = position

def add_metadata(frame):
    timestamp = time.time()
    position = "lat 10 long 20"
    return Frame_data(frame, timestamp, position)

def camera_process_func(queue, ip, port, user, password):
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    cap = cv2.VideoCapture(str(cam_link))
    while(True):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        data_for_consumer = add_metadata(frame)
        print(data_for_consumer.timestamp, data_for_consumer.position)
        #cv2.imshow('frame',frame)
        #cv2.imwrite('frames/gr'+str(i)+'.jpg', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()