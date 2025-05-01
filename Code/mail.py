
import smtplib
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetching credentials from environment variables
sender_email = os.getenv('EMAIL_USER')
sender_password = os.getenv('EMAIL_PASSWORD')
recipient_email = 'agentravaan@gmail.com'

subject = '🚨 Intruder Alert!'
body = 'Motion detected! See attached frames.'

def send_email(frames, sender_email, sender_password, recipient_email, subject, body):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach frames as images
        for i, frame in enumerate(frames):
            success, frame_jpeg = cv2.imencode(".jpg", frame)
            if success:  
                image = MIMEImage(frame_jpeg.tobytes())
                image.add_header("Content-Disposition", "attachment", filename=f"frame{i+1}.jpg")
                msg.attach(image)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("📩 Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
