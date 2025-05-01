from cryptography.fernet import Fernet
import cv2
import numpy as np
import os
from datetime import datetime

# Generate a key for encryption and decryption (you should store this key securely)
# If you already have a key saved, you can use that instead of generating a new one each time.
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# Function to save the encrypted frame
def save_encrypted_frame(frame, filename):
    # Convert the frame to bytes
    _, buffer = cv2.imencode(".jpg", frame)
    frame_bytes = buffer.tobytes()

    # Encrypt the frame bytes
    key = load_key()  # Load the encryption key
    cipher = Fernet(key)
    encrypted_frame = cipher.encrypt(frame_bytes)

    # Save the encrypted frame to a file
    with open(filename, "wb") as enc_file:
        enc_file.write(encrypted_frame)

    print(f"Encrypted frame saved as {filename}")

# Function to decrypt an encrypted frame (for later use if needed)
def decrypt_frame(filename):
    # Load the encrypted frame
    with open(filename, "rb") as enc_file:
        encrypted_frame = enc_file.read()

    # Decrypt the frame
    key = load_key()  # Load the encryption key
    cipher = Fernet(key)
    decrypted_frame_bytes = cipher.decrypt(encrypted_frame)

    # Convert the decrypted bytes back to an image
    nparr = np.frombuffer(decrypted_frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return frame

# Optionally, if you haven't generated the key already, uncomment the next line:
# generate_key()
