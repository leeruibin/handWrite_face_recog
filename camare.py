import cv2

def func():
    faceCascade = cv2.CascadeClassifier('./config/haarcascade_frontalface_alt2.xml')
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("Video",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video", 379, 676)
    cv2.moveWindow("Video", 437, 190)
    while True:
       # Capture frame-by-frame
       ret, frame = video_capture.read()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = faceCascade.detectMultiScale(
           gray,
           scaleFactor=1.1,
           minNeighbors=5,
           minSize=(30, 30),
           flags=cv2.CASCADE_SCALE_IMAGE
       )
       # Draw a rectangle around the faces
       for (x, y, w, h) in faces:
          cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

       # Display the resulting frame
       cv2.imshow('Video', frame)
       k = cv2.waitKey(1) & 0xff
       if k==ord('q'):
           break
       elif k==ord(' '):
           ret, frame = video_capture.read()
           cv2.imwrite('./picture/face.jpg', frame)
           break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()