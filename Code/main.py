import cv2
import face_recognition
import numpy as np
import os
import threading
from playsound import playsound
import mail
from sklearn.metrics import precision_score, recall_score, f1_score
import encryption  # Import encryption process
from datetime import datetime
import winsound

beep_thread = None

# Load known faces and their encodings
KNOWN_FACES_DIR = r'D:\Desktop\Update_Project\User Pictures'
known_faces = []
known_names = []

print("Loading known faces...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith('.jpeg') or filename.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_faces.append(encoding[0])
            known_names.append(filename.split('.')[0])  # Use filename without extension as name

print(f"Loaded {len(known_faces)} known faces.")

# Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # For Windows

if not cap.isOpened():
    print("Error: Camera not found!")
    exit()

# Initialize variables
alarm_mode = False
alarm = False
alarm_counter = 0
y_true = []  # True labels (1 for authorized, 0 for unauthorized)
y_pred = []  # Predicted labels (1 for match, 0 for no match)

# Beep alarm function (with fixed playsound handling)
def beep_alarm():
    global alarm
    while alarm_mode:
        try:
            winsound.PlaySound(r'D:\Desktop\Update_Project\alarm.mp3', winsound.SND_FILENAME)
        except Exception as e:
            print(f"Error playing sound: {e}")
            break

# Function to save encrypted frames
def save_encrypted_frame(frame):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"frame_{timestamp}.enc"
    encryption.save_encrypted_frame(frame, filename)  # Call the encryption function to save the frame

# Start face recognition loop
while True:
    _, frame = cap.read()
    
    if frame is None:
        print("Error: Failed to capture image from camera.")
        break

    # Resize and convert to RGB
    frame_resized = cv2.resize(frame, (500, 500))
    rgb_frame = frame_resized[:, :, ::-1]

    # Find all faces in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, encoding)

        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            y_true.append(1)  # Authorized user
            y_pred.append(1)  # Prediction match
        else:
            y_true.append(0)  # Unauthorized user
            y_pred.append(0)  # Prediction match

            if not alarm:
                print("⚠ ALERT! Unknown person detected! ⚠")
                alarm = True
                alarm_mode = True
                if beep_thread is None or not beep_thread.is_alive():
                    beep_thread = threading.Thread(target=beep_alarm)
                    beep_thread.start()

                # Save encrypted frame of the unknown person
                save_encrypted_frame(frame)

                # Send email with the frame captured
                recipient_email = "agentravaan@gmail.com"  # Replace with actual recipient email
                subject = "Unknown Person Alert"
                body = "An unknown person has been detected in front of the camera."
                threading.Thread(target=mail.send_email, args=([frame], "shivaramravuri@gmail.com", "tfnp lbtv hkvh tpbn", recipient_email, subject, body)).start()

        # Draw rectangle around face and label
        cv2.rectangle(frame_resized, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame_resized, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Show the resulting image
    cv2.imshow("Cam", frame_resized)

    # Print evaluation metrics when an unknown person is detected
    if len(y_true) > 0 and len(y_pred) > 0:
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        print(f"Face Recognition - Precision: {precision}, Recall: {recall}, F1-Score: {f1}")

    # Break the loop if 'q' is pressed
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('q'):
        print("Quitting the program!")
        alarm_mode = False  # Turn off alarm mode
        break

cap.release()
cv2.destroyAllWindows()
