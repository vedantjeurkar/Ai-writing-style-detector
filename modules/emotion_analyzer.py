
from transformers import pipeline

_emotion_model = None  # Cached model

def load_emotion_model():
    """Loads emotion detection model (downloads first time)."""
    global _emotion_model
    if _emotion_model is None:
        _emotion_model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None  # Return ALL emotions with their scores
        )
    return _emotion_model

def analyze_emotion(text):
    """
    Takes text as input.
    Returns a dictionary with:
    - dominant_emotion: the strongest emotion detected
    - emotion_scores: all 7 emotions with percentages
    - tone: formal/casual/neutral
    - tone_description: a sentence describing the tone

    Example output:
    {
        "dominant_emotion": "joy",
        "emotion_emoji": "😊",
        "emotion_scores": {"joy": 72, "neutral": 15, "sadness": 8, ...},
        "tone": "Casual & Upbeat",
        "tone_description": "The writer sounds enthusiastic and informal"
    }
    """
    model = load_emotion_model()

    # Run model — returns list of all emotions with scores
    
    results = model(text[:512])[0]

    # Convert to a simple dictionary: {"joy": 72, "sadness": 8, ...}
    emotion_scores = {
        item["label"]: round(item["score"] * 100)
        for item in results
    }

    # Find the strongest emotion
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Emoji mapping for each emotion
    emoji_map = {
        "joy": "😊",
        "sadness": "😢",
        "anger": "😠",
        "fear": "😨",
        "surprise": "😲",
        "disgust": "🤢",
        "neutral": "😐"
    }

    emotion_emoji = emoji_map.get(dominant_emotion, "🎭")

    # Determine tone based on emotion
    tone, tone_description = _determine_tone(dominant_emotion, text)

    return {
        "dominant_emotion": dominant_emotion.capitalize(),
        "emotion_emoji": emotion_emoji,
        "emotion_scores": emotion_scores,
        "tone": tone,
        "tone_description": tone_description
    }

def _determine_tone(dominant_emotion, text):
    """
    Determines the writing tone based on dominant emotion
    and text characteristics.
    Returns (tone_label, tone_description)
    """
    text_lower = text.lower()

    # Check formality clues
    formal_words = ["therefore", "furthermore", "consequently", "hereby", "pursuant"]
    casual_words = ["hey", "yeah", "gonna", "wanna", "lol", "omg", "btw"]

    is_formal = any(w in text_lower for w in formal_words)
    is_casual = any(w in text_lower for w in casual_words)

    # Combine emotion + formality to get tone
    tone_map = {
        "joy": ("Upbeat & Enthusiastic", "The writer sounds excited and positive"),
        "sadness": ("Melancholic & Reflective", "The writer sounds sad or introspective"),
        "anger": ("Assertive & Intense", "The writer sounds frustrated or confrontational"),
        "fear": ("Anxious & Cautious", "The writer sounds worried or uncertain"),
        "surprise": ("Expressive & Reactive", "The writer sounds shocked or amazed"),
        "disgust": ("Critical & Disapproving", "The writer sounds disapproving or repulsed"),
        "neutral": ("Calm & Composed", "The writer maintains a balanced, neutral tone")
    }

    tone_label, tone_desc = tone_map.get(dominant_emotion, ("Neutral", "Balanced tone"))

    # Add formality layer
    if is_formal:
        tone_label = "Formal & " + tone_label
    elif is_casual:
        tone_label = "Casual & " + tone_label.split(" & ")[-1]

    return tone_label, tone_desc
