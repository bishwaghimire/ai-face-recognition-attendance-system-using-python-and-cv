import cv2
import face_recognition
import pickle
import numpy as np
import customtkinter as ctk
from attendance import mark_attendance

# Load saved encodings
with open("encodings/encodings.pkl", "rb") as file:
    data = pickle.load(file)

known_encodings = data["encodings"]
known_names = data["names"]
known_rolls = data["rolls"]

# Global variables
video = None
camera_running = False


def start_recognition(camera_label=None,
                      detected_label=None,
                      status_label=None,
                      update_ui_callback=None):

    global video, camera_running

    if camera_running:
        print("Camera is already running.")
        return

    camera_running = True

    video = cv2.VideoCapture(0)

    # Set frame dimensions for stability
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Starting Face Recognition...")

    while camera_running:

        success, frame = video.read()

        # if not success:
        #     print("Failed to read webcam")
        #     break

        if not success:
            # Instead of break, warn and skip to the next iteration
            print("Warning: Dropped frame or failed to read webcam. Retrying...")
            cv2.waitKey(10)
            continue

        # Resize for faster processing
        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.25,
            fy=0.25
        )

        # Convert BGR to RGB
        rgb_small_frame = cv2.cvtColor(
            small_frame,
            cv2.COLOR_BGR2RGB
        )

        # Detect face locations
        face_locations = face_recognition.face_locations(
            rgb_small_frame
        )

        # Generate encodings
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations
        )

        # Process each detected face
        for face_encoding, face_location in zip(
            face_encodings,
            face_locations
        ):

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

                mark_attendance(roll, name)

                if detected_label:
                    detected_label.configure(
                        text=f"Detected: {name}"
                    )

                if status_label:
                    status_label.configure(
                        text="Attendance Marked",
                        text_color="green"
                    )

                # --- NEW: Update the Scrollable List ---
                if update_ui_callback:
                    update_ui_callback(roll, name)

            # Scale coordinates back
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

        # If GUI exists
        if camera_label:

            from PIL import Image

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(rgb_frame)

            # This makes the image fill the frame nicely
            # We calculate size based on label width to keep it 'Large'
            aspect_ratio = frame.shape[1] / frame.shape[0]
            display_width = camera_label.winfo_width()
            display_height = int(display_width / aspect_ratio)

            # Get current display dimensions of the image
            h, w, _ = frame.shape

            # Use CTkImage instead of ImageTk.PhotoImage
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(display_width, display_height))

            camera_label.configure(image=ctk_img)
            camera_label.imgtk = ctk_img


        else:
            # Normal OpenCV window
            cv2.imshow(
                "Face Recognition Attendance System",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    stop_recognition()


def stop_recognition():
    global camera_running, video
    camera_running = False
    if video:
        video.release()
        video = None
    cv2.destroyAllWindows()
    print("Camera stopped.")