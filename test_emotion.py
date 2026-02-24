"""
Quick test script for emotion detection
Run: python test_emotion.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIC.settings')
django.setup()

from User.emotion_detector import get_emotion_detector

def test_emotions():
    print("Loading emotion detector...")
    detector = get_emotion_detector()
    print("✓ Model loaded successfully!\n")
    
    test_messages = [
        "I'm so happy today! Everything is going great!",
        "I feel really sad and lonely right now.",
        "I'm worried about what might happen tomorrow.",
        "This is just a normal day, nothing special.",
        "I can't believe this happened! I'm so angry!",
    ]
    
    print("Testing emotion detection:\n")
    for msg in test_messages:
        emotion, confidence, sentiment = detector.predict(msg)
        print(f"Message: {msg}")
        print(f"Emotion: {emotion} ({confidence*100:.1f}%)")
        print(f"Sentiment: {sentiment}")
        print("-" * 60)

if __name__ == "__main__":
    test_emotions()
