import cv2
import time
import os

face_cascade = "haarcascade_frontalface_default.xml"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'cascades/')
file_path = UPLOAD_FOLDER + face_cascade

VIDEO_FOLDER = os.path.join(APP_ROOT, 'Input/')
video = VIDEO_FOLDER + 'Megamind.avi'

def generate():

# Nacitanie KASKADY
  face_cascade = cv2.CascadeClassifier(file_path)

# VSTUP

  cap = cv2.VideoCapture(video)


  while(cap.isOpened()):
    ret, img = cap.read()

    if ret == True:

      img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# FACE DETECTION
      faces = face_cascade.detectMultiScale(gray, 1.1, 6)

      for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

# SENDING FRAMES
      frame = cv2.imencode('.jpg', img)[1].tobytes()
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
      time.sleep(0.03)

    else:
      cap.release()
      cv2.destroyAllWindows()
