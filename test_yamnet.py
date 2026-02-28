import tensorflow_hub as hub
import numpy as np
import csv
import librosa

model = hub.load('https://tfhub.dev/google/yamnet/1')

class_names = []
with open('yamnet_classes.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        class_names.append(row[2])

# These are the danger sounds RakshaAI watches for
DANGER_SOUNDS = ['Screaming', 'Crying, sobbing', 'Shout', 'Yell', 'Whimper, sob', 'Wail, moan']

def get_danger_score(audio_path):
    audio, sr = librosa.load(audio_path, sr=16000, mono=True)
    audio = audio.astype(np.float32)

    scores, embeddings, spectrogram = model(audio)
    mean_scores = np.mean(scores.numpy(), axis=0)

    # Calculate danger score from scream-related sounds
    danger_score = 0.0
    for i, name in enumerate(class_names):
        if name in DANGER_SOUNDS:
            danger_score += mean_scores[i]

    # Top 3 sounds detected
    top3 = np.argsort(mean_scores)[::-1][:3]

    return danger_score, [(class_names[i], mean_scores[i]) for i in top3]

# Test it
score, top_sounds = get_danger_score(r'C:\Users\dhruv\Downloads\RakshaAI_system\scream_converted.wav')

print("Top 3 detected sounds:")
for name, confidence in top_sounds:
    print(f"  {name}: {confidence:.3f}")

print(f"\nDanger Score: {score:.3f}")

if score > 0.3:
    print("⚠️  DANGER DETECTED — Trigger SOS!")
else:
    print("✅ Safe — No danger detected")
