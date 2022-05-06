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


#gets stream link, starts the capture, adds metadata to each frame and sends it to the queue
def camera_process_func(queue, ip, port, user, password):
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    cap = cv2.VideoCapture(str(cam_link))
    #while(True):
    for i in range(30):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        data_for_consumer = add_metadata(frame)
        queue.put(data_for_consumer)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()