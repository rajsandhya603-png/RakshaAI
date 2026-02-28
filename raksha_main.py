import tensorflow_hub as hub
import numpy as np
import csv
import librosa
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# ── CONFIG ──────────────────────────────────────────
SENDER_EMAIL   = "rajsandhya603@gmail.com"
APP_PASSWORD   = "wfcgxocttkipoeka"
RECEIVER_EMAIL = "rajsandhya603@gmail.com"  # trusted contact email
LATITUDE       = 21.1702
LONGITUDE      = 72.8311
RISK_THRESHOLD = 0.7
# ────────────────────────────────────────────────────

print("Loading YAMNet model...")
model = hub.load('https://tfhub.dev/google/yamnet/1')

class_names = []
with open('yamnet_classes.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        class_names.append(row[2])

DANGER_SOUNDS = ['Screaming', 'Crying, sobbing', 'Shout', 'Yell', 'Whimper, sob', 'Wail, moan']

def get_sound_score(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    audio = audio.astype(np.float32)
    scores, _, _ = model(audio)
    mean_scores = np.mean(scores.numpy(), axis=0)
    danger_score = sum(mean_scores[i] for i, name in enumerate(class_names) if name in DANGER_SOUNDS)
    return round(float(danger_score), 3)

def calculate_risk(sound_score, motion_spike=False, hour=None, location_anomaly=False):
    import datetime
    if hour is None:
        hour = datetime.datetime.now().hour

    if hour >= 22 or hour <= 5:
        time_score = 1.0
    elif hour >= 20 or hour <= 7:
        time_score = 0.5
    else:
        time_score = 0.1

    risk = (
        sound_score              * 0.40 +
        (1.0 if motion_spike else 0.0)   * 0.30 +
        time_score               * 0.20 +
        (1.0 if location_anomaly else 0.0) * 0.10
    )
    return round(risk, 3)

def send_sos_email():
    subject = "RAKSHA AI - EMERGENCY ALERT!"
    body = f"""
    EMERGENCY DETECTED!
    
    RakshaAI has detected a dangerous situation.
    
    Live Location: https://maps.google.com/?q={LATITUDE},{LONGITUDE}
    
    Please respond immediately!
    
    - RakshaAI System
    """
    msg = MIMEMultipart()
    msg['From']    = SENDER_EMAIL
    msg['To']      = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("SOS Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def analyze_audio(audio_path):
    print(f"\nAnalyzing: {audio_path}")
    
    sound_score = get_sound_score(audio_path)
    risk_score  = calculate_risk(sound_score)
    
    print(f"Sound Score : {sound_score}")
    print(f"Risk Score  : {risk_score}")
    
    if risk_score >= RISK_THRESHOLD:
        print("DANGER DETECTED - Sending SOS!")
        send_sos_email()
    else:
        print("Safe - No danger detected")

# ── TEST ─────────────────────────────────────────────
# Simulate a danger scenario directly
print("\n--- Simulating DANGER scenario ---")
risk_score = calculate_risk(sound_score=0.9, motion_spike=True, hour=23)
print(f"Risk Score: {risk_score}")
if risk_score >= RISK_THRESHOLD:
    print("DANGER DETECTED - Sending SOS!")
    send_sos_email()
else:
    print("Safe")