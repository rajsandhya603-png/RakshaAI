
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
SENDER_EMAIL = "rajsandhya603@gmail.com"
APP_PASSWORD = "wfcgxocttkipoeka"

def send_sos_email(receiver_email, latitude, longitude):
    subject = "🚨 RAKSHA AI - EMERGENCY ALERT!"
    
    body = f"""
    EMERGENCY DETECTED!
    
    RakshaAI has detected a dangerous situation.
    
    📍 Live Location: https://maps.google.com/?q={latitude},{longitude}
    
    Please respond immediately and contact the person or call police.
    
    - RakshaAI System
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ SOS Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Test it — sends to yourself first
send_sos_email("rajsandhya603@gmail.com", 21.1702, 72.8311)