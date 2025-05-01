# Trustworthy-Evaluation-Of-Motion-Detection-and-Intrusion-Alert-System
A motion detection and intrusion alert system focused on trustworthy evaluation. This project evaluates trustworthiness aspects of AI-powered surveillance, specifically privacy, robustness, and security. The system uses advanced models like YOLOv8 to ensure reliable motion detection, while prioritizing data protection and ethical AI practices.

---
## 📌 Overview
This project is a **Motion Detection and Intrusion Alert System** that:
- Detects motion using a webcam.
- Recognizes known faces and triggers an alarm for unknown faces.
- Sends an email alert with captured frames if an unknown person is detected.
- Plays an alert sound when an unknown face is detected.
- Encrypting the detected frames using Fernet Algorithm.
- Also, Decrypting the encrypted image.
- Robustness evaluation of model under the scenarios such as Blur images, Occlusion Images, Noise Images, Lighting Images.
- Model Enhancement.

---
### 2️⃣ Install Required Dependencies
Run the following command to install all necessary packages:
```bash
pip install -r requirements.txt
```
**OR** manually install them:
```bash
pip install opencv-python numpy imutils matplotlib seaborn pandas scikit-learn face-recognition threading datetime dlib playsound smtplib python-dotenv email email-validator cryptography
```

If you encounter issues with `dlib`, install CMake first:
```bash
# For MacOS
brew install cmake

# For Ubuntu/Linux
sudo apt-get install cmake
```

---
### 3️⃣ Set Up Email Alerts
To receive email alerts, you need to set up your **Gmail App Password**:

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
2. Select "Mail" as the app and "Other (Custom name)" as the device.
3. Generate a password and **copy it**.
4. Open `mail.py` and replace:
   ```python
   sender_email = 'your-email@gmail.com'
   sender_password = 'your-app-password'
   recipient_email = 'recipient-email@gmail.com'
   ```
---

## 🚀 Running the Application
Once everything is set up, run the script using:
```bash
python Secret_Key.py
```
### Expected Outcome:
- It will generate a Secret Key for Encryption.
Then Run the main file:
```bash
python main.py
```
### Expected Behavior:
- The webcam will start capturing frames.
- If a **known face** is detected → **No alarm**.
- If an **unknown face** is detected → **Alarm sound & Email Alert Sent**.
- Email will contain the captured frames of the unknown person.
- Detected Frame will be Encrypted By Fernet Algorithm using Secret Key.

To stop the program, press **'Q'**.

For getting the original detected image after encryption:
```bash
python decription.py
```
### Expected Outcome:
- It will generate Original Frame.


To Evaluate the Robusteness of the Model, Run the following Scripts:
```bash
python robustness_test_webcam.py

#Press l for Lighting, n for noise, o for occlusion, and b for blur scenario's image capturing
```
### Expected Outcome:
- It will prompt the webcam capturing the frames with option of blur, lighting, occlusion, noise options

For Analysis:
```bash
python analyze_robustness.py
```
### Expected Outcome:
- It will produce the Results in the form of Heatmap, Bar Charts of the measures of Total Frames, Detection Rate, Scenarios 
---

## 🛠 Customization
### ✅ Adding Known Faces
1. Create a folder called `known_faces`.
2. Add images of known people inside the folder.
3. Update `main.py` to load these faces automatically.

### ✅ Changing Alert Sound
Replace `alert.mp3` with your custom alert sound.

---

## ⚠️ Troubleshooting
- **No email received?**
  - Check if you've enabled **Less Secure Apps** or used an **App Password**.
  - Make sure your email credentials are correct.
  - Check spam folder.
- **Camera not detected?**
  - Ensure the webcam is properly connected.
  - Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.
- **Face recognition not working?**
  - Ensure `known_faces` folder has clear images.
  - Improve accuracy by adding more training images per person.

---

## Acknowledgments
This project uses:
- [YOLOv8](https://github.com/ultralytics/yolov8) for motion detection.
- Some parts of the alert system were adapted from [OpenCV Motion Detection](https://github.com/opencv/opencv).
