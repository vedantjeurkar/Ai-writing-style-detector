
from transformers import pipeline

_detector = None  # We store the model here after first load

def load_detector():
    """
    Loads the AI detection model.
    First time: downloads from internet (~500MB), takes 1-2 min.
    After that: loads from cache instantly.
    """
    global _detector
    if _detector is None:
        # text-classification = model that puts text into categories
        _detector = pipeline(
            "text-classification",
            model="roberta-base-openai-detector"
        )
    return _detector

def detect_ai(text):
    """
    Takes text as input.
    Returns a dictionary with:
    - verdict: "AI Written" or "Human Written"
    - ai_score: probability it's AI (0 to 100)
    - human_score: probability it's human (0 to 100)
    - confidence: how sure the model is
    - signals: list of observations about the text

    Example output:
    {
        "verdict": "AI Written",
        "ai_score": 82,
        "human_score": 18,
        "confidence": "High",
        "signals": ["Very consistent tone", "Long structured sentences"]
    }
    """
    detector = load_detector()

    result = detector(text[:512])[0]  # [:512] = only use first 512 chars (model limit)

    label = result["label"]   # "FAKE" or "REAL"
    score = result["score"]   # confidence between 0 and 1

    # Convert to percentages and human-readable labels
    if label == "FAKE":
        # Model says it's AI-written
        ai_score = round(score * 100)
        human_score = 100 - ai_score
        verdict = "🤖 AI Written"
    else:
        # Model says it's human-written
        human_score = round(score * 100)
        ai_score = 100 - human_score
        verdict = "✍️ Human Written"

    # Determine confidence level
    if score > 0.85:
        confidence = "High"
    elif score > 0.65:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Generate observations about the text
    signals = _generate_signals(text, label)

    return {
        "verdict": verdict,
        "ai_score": ai_score,
        "human_score": human_score,
        "confidence": confidence,
        "signals": signals
    }

def _generate_signals(text, label):
    """
    Generates human-readable observations about why
    the model thinks it's AI or Human written.
    These are based on common patterns in AI vs human text.
    """
    signals = []
    words = text.split()
    sentences = text.split(".")

    avg_sentence_length = len(words) / max(len(sentences), 1)

    # Check for common AI writing patterns
    if avg_sentence_length > 20:
        signals.append("📏 Long, structured sentences (common in AI text)")

    if avg_sentence_length < 10:
        signals.append("✂️ Short, punchy sentences (more human-like)")

    # Check for filler words common in human writing
    human_words = ["honestly", "i think", "i feel", "you know", "like", "actually", "basically"]
    found_human = [w for w in human_words if w in text.lower()]
    if found_human:
        signals.append(f"💬 Casual/filler words found: {', '.join(found_human[:3])}")

    # Check for AI-typical formal phrases
    ai_phrases = ["furthermore", "in conclusion", "it is important", "notably", "additionally"]
    found_ai = [p for p in ai_phrases if p in text.lower()]
    if found_ai:
        signals.append(f"📋 Formal AI-typical phrases: {', '.join(found_ai[:3])}")

    # Check text length
    if len(words) < 30:
        signals.append("⚠️ Text is short — results may be less accurate")

    if not signals:
        signals.append("🔍 No strong signals detected — borderline case")

    return signals
