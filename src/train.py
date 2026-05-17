import os
import cv2
import face_recognition
import pickle

DATASET_PATH = "../datasets"

known_encodings = []
known_names = []
known_rolls = []

# Loop through dataset folders
for folder_name in os.listdir(DATASET_PATH):

    folder_path = os.path.join(DATASET_PATH, folder_name)

    if not os.path.isdir(folder_path):
        continue

    # Example: 01_rajesh_hamal
    parts = folder_name.split("_", 1)

    roll = parts[0]
    name = parts[1]

    print(f"\nProcessing: {name}")

    # Read all images inside folder
    for image_name in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image_name)

        # Load image
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read {image_name}")
            continue

        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations
        face_locations = face_recognition.face_locations(rgb_image)

        if len(face_locations) == 0:
            print(f"No face found in {image_name}")
            continue

        # Generate face encodings
        face_encodings = face_recognition.face_encodings(
            rgb_image,
            face_locations
        )

        for encoding in face_encodings:

            known_encodings.append(encoding)
            known_names.append(name)
            known_rolls.append(roll)

            print(f"Encoded: {image_name}")

# Save encodings
data = {
    "encodings": known_encodings,
    "names": known_names,
    "rolls": known_rolls
}

with open("encodings.pkl", "wb") as file:
    pickle.dump(data, file)

print("\nTraining Complete!")
print(f"Total encodings: {len(known_encodings)}")