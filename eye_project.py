import cv2

# Load the Haar cascade classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Function to detect eyes state
def detect_eyes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
    
        if len(eyes)==0:
            print ("eyes are not detected")
        elif len(eyes)>1:
            print("eyes are detected")
        else:
            for (ex, ey, ew, eh) in eyes:
             # Draw rectangles around the eyes
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

            # Calculate aspect ratio (height / width) of eye region
                aspect_ratio = float(eh) / ew

            # If the aspect ratio is below a certain threshold, eyes are considered closed
                if aspect_ratio > 1:
                    cv2.putText(image, 'Eyes Closed', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(image, 'Eyes Open', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame from the video capture
    ret, frame = cap.read()

    # Skip iteration if frame read is unsuccessful
    if not ret:
        continue

    # Flip the frame horizontally for a mirror-like effect
    frame = cv2.flip(frame, 1)

    # Detect eyes and display the result
    frame = detect_eyes(frame)

    # Display the resulting frame
    cv2.imshow('Driver Monitoring', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
