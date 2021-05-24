import cv2
import time
import os

face_cascade = "haarcascade_frontalface_default.xml"
eye_cascade = "haarcascade_eye_tree_eyeglasses.xml"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'cascades/')

file_path = UPLOAD_FOLDER + face_cascade
file_path1 = UPLOAD_FOLDER + eye_cascade

VIDEO_FOLDER = os.path.join(APP_ROOT, 'Input/')
video = VIDEO_FOLDER + 'Megamind.avi'

def generate1():
# Nacitanie kaskad
  face_cascade = cv2.CascadeClassifier(file_path)
  eye_cascade = cv2.CascadeClassifier(file_path1)

# VSTUP
  cap = cv2.VideoCapture(video)

  while(cap.isOpened()):
    ret, img = cap.read()

    if ret == True:
      img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      # FACE DETECTION
      faces = face_cascade.detectMultiScale(gray, 1.1, 4)

      for (x, y, w, h) in faces:

        # show in gray point of interest
        roi_gray = gray[y:y+h, x:x+w]
        # show in color point of interest
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 3)
        # sending data
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.01)

    else:
      cap.release()
      cv2.destroyAllWindows()
