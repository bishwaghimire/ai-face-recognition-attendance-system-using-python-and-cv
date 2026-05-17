import cv2
import face_recognition
import pickle
import numpy as np
from attendance import mark_attendance

# Load saved encodings
with open("encodings/encodings.pkl", "rb") as file:
    data = pickle.load(file)

known_encodings = data["encodings"]
known_names = data["names"]
known_rolls = data["rolls"]

# Open webcam
video = cv2.VideoCapture(0)

print("Starting Face Recognition...")

while True:

    success, frame = video.read()

    if not success:
        print("Failed to read webcam")
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR to RGB
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    face_locations = face_recognition.face_locations(rgb_small_frame)

    # Generate encodings
    face_encodings = face_recognition.face_encodings(
        rgb_small_frame,
        face_locations
    )

    # Process each detected face
    for face_encoding, face_location in zip(face_encodings, face_locations):

        # Compare with known faces
        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        face_distances = face_recognition.face_distance(
            known_encodings,
            face_encoding
        )

        best_match_index = np.argmin(face_distances)

        name = "Unknown"
        roll = ""

        if matches[best_match_index]:
            name = known_names[best_match_index]
            roll = known_rolls[best_match_index]

            # Mark attendance
            mark_attendance(roll, name)

        # Scale face coordinates back
        top, right, bottom, left = face_location

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle
        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        # Draw label
        label = f"{roll} - {name}"

        cv2.putText(
            frame,
            label,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Show webcam
    cv2.imshow("Face Recognition Attendance System", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
video.release()
cv2.destroyAllWindows()