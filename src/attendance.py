import csv
import os
from datetime import datetime

ATTENDANCE_FOLDER = "attendance"

# Create attendance folder if not exists
os.makedirs(ATTENDANCE_FOLDER, exist_ok=True)


def mark_attendance(roll, name):

    # Current date
    date_today = datetime.now().strftime("%Y-%m-%d")

    # File name based on date
    filename = f"{ATTENDANCE_FOLDER}/{date_today}.csv"

    # Track if the file already exists before we open it
    file_exists = os.path.exists(filename)
    
    # Check existing entries to prevent duplicate attendance
    existing_rolls = []
    if file_exists:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 0:
                    existing_rolls.append(row[0])

    # Prevent duplicate attendance
    if str(roll) in existing_rolls:
        return

    # Current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Write attendance
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        # Write header ONLY if this is a brand new file for the day
        if not file_exists:
            writer.writerow(["Roll no", "Name", "Time", "Date"])

        # Write the student's data row
        writer.writerow([
            roll,
            name,
            current_time,
            date_today
        ])

    print(f"Attendance Marked: {roll} - {name}")