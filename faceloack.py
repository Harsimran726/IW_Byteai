import cv2
import face_recognition
import os
import testing
# Create a directory to store captured faces
if not os.path.exists("captured_faces"):
    os.makedirs("captured_faces")

# Initialize webcam
cap = cv2.VideoCapture(0)




# Load known faces
known_faces = []
known_face_names = []

# Load known faces from the "known_faces" directory
def load_known_faces(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            image = face_recognition.load_image_file(os.path.join(directory, filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_face_names.append(filename.split('.')[0])
 # Load known faces from the directory
load_known_faces("known_faces")
while True:
    ret, frame = cap.read()

    # Find face locations in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"


        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            #cv2.rectangle(frame, (left, top), (right, bottom), (102, 205, 0), 2)

        # Draw a rectangle around the face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (121,205,205), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Press 'c' to capture and save the user's face
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Capture and save the face data
        if len(face_locations) == 1:
            captured_face = frame[top:bottom, left:right]
            if captured_face.shape[0] > 0 and captured_face.shape[1] > 0:
                cv2.imwrite(os.path.join("known_faces", "user_face.jpg"), captured_face)
                print("User's face captured and saved!")

    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
