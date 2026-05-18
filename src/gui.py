import customtkinter as ctk
import threading
from recognize import start_recognition, stop_recognition

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main Window
app = ctk.CTk()
app.title("AI Face Recognition Attendance System")
app.geometry("1300x700") # Increased width for the list

# -----------------------------
# Title
# -----------------------------

title = ctk.CTkLabel(
    app,
    text="AI Face Recognition Attendance System",
    font=("Arial", 30, "bold")
)

title.pack(pady=10)

# -----------------------------
# Main Frame
# -----------------------------

main_frame = ctk.CTkFrame(app)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# --- Left Side (Camera) ---
left_frame = ctk.CTkFrame(main_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

camera_label = ctk.CTkLabel(left_frame, text="Camera Feed Loading...", font=("Arial", 16))
camera_label.pack(fill="both", expand=True)

# -----------------------------
# Right Side
# -----------------------------

# --- Right Side (Controls & List) ---
right_frame = ctk.CTkFrame(main_frame, width=600)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

detected_label = ctk.CTkLabel(right_frame, text="Detected: None", font=("Arial", 20, "bold"))
detected_label.pack(pady=10)

status_label = ctk.CTkLabel(right_frame, text="System Ready", font=("Arial", 16))
status_label.pack(pady=5)


# --- NEW: Present Students List ---
ctk.CTkLabel(right_frame, text="Today's Attendance:", font=("Arial", 16, "underline")).pack(pady=(20, 5))
attendance_list = ctk.CTkScrollableFrame(right_frame, width=550, height=300)
attendance_list.pack(pady=10, padx=10, fill="both", expand=True)

# Helper function to update the list from the recognition thread
def update_attendance_ui(roll, name):
    # Check if student is already in the UI list to avoid visual duplicates
    exists = False
    for child in attendance_list.winfo_children():
        if child.cget("text") == f"{roll} - {name}":
            exists = True
            break
    
    if not exists:
        entry = ctk.CTkLabel(attendance_list, text=f"{roll} - {name}", font=("Arial", 14), anchor="w")
        entry.pack(fill="x", pady=2)

# -----------------------------
# Buttons
# -----------------------------

def start_camera():
    # Check if a camera thread is already active globally
    # import recognize
    # if recognize.camera_running:
    #     status_label.configure(text="Camera already running!", text_color="yellow")
    #     return

    # status_label.configure(text="Starting Camera...", text_color="white")
    
    thread = threading.Thread(
        target=start_recognition,
        args=(
            camera_label,
            detected_label,
            status_label,
            update_attendance_ui
        )
    )
    thread.daemon = True
    thread.start()


start_btn = ctk.CTkButton(
    right_frame,
    text="Start Camera",
    command=start_camera,
    width=520,
    height=50
)

start_btn.pack(pady=20)

stop_btn = ctk.CTkButton(
    right_frame,
    text="Stop Camera",
    command=stop_recognition,
    width=520,
    height=50
)

stop_btn.pack(pady=20)

exit_btn = ctk.CTkButton(
    right_frame,
    text="Exit",
    command=app.destroy,
    width=500,
    height=50,
    fg_color="red"
)

exit_btn.pack(pady=20)

# -----------------------------
# Run App
# -----------------------------

app.mainloop()