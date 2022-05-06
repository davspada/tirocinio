import cv2
import camera_operations

def camera_process_func(ip, port, user, password):
    cam_link = camera_operations.getStreamLink(ip, port, user, password)
    cap = cv2.VideoCapture(str(cam_link))
    while(True):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        cv2.imshow('frame',frame)
        #cv2.imwrite('frames/gr'+str(i)+'.jpg', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()