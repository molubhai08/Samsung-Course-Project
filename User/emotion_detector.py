import torch
import os
from transformers import BertTokenizerFast, BertForSequenceClassification

# Emotion mapping - simplified to 3 categories
POSITIVE_EMOTIONS = ['Positive', 'Curiosity', 'Desire', 'Surprise']
NEGATIVE_EMOTIONS = ['Negative', 'Sadness', 'Fear']
NEUTRAL_EMOTIONS = ['Neutral', 'Confusion']

class EmotionDetector:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model', 'emotion_model_final')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = BertTokenizerFast.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        # Get label mapping from model config
        self.id2label = self.model.config.id2label

    def predict(self, text):
        """
        Predict emotion for a single text.
        Returns: (emotion_category, confidence_score, sentiment_type)
        sentiment_type: 'Positive', 'Negative', or 'Neutral' (capitalized for display)
        """
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=128
        ).to(self.device)
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
        top_idx = probs.argmax()
        emotion = self.id2label[top_idx]
        confidence = float(probs[top_idx])
        
        # Map to simplified sentiment - return capitalized for display
        if emotion in POSITIVE_EMOTIONS:
            sentiment = 'Positive'
        elif emotion in NEGATIVE_EMOTIONS:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return sentiment, confidence, sentiment.lower()

# Global instance
_detector = None

def get_emotion_detector():
    global _detector
    if _detector is None:
        _detector = EmotionDetector()
    return _detector
