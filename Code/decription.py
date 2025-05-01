from cryptography.fernet import Fernet
import cv2
import numpy as np

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# Function to decrypt an encrypted frame
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

# Save the decrypted frame as an image
def save_decrypted_frame(frame, filename):
    cv2.imwrite(filename, frame)
    print(f"Decrypted frame saved as {filename}")

# Example usage
if __name__ == "__main__":
    encrypted_file = "frame_20250427_125334.enc"  # Encrypted file
    decrypted_file = "decrypted_frame.jpg"  # Decrypted file to save

    # Decrypt the frame
    decrypted_frame = decrypt_frame(encrypted_file)

    # Save the decrypted frame
    save_decrypted_frame(decrypted_frame, decrypted_file)
