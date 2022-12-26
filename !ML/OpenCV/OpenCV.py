import cv2

# Load the Haar cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Create a VideoCapture object to access the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    _, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Check if the user pressed the Esc key
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()
