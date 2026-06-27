
def tag_writing_style(text):
    """
    Takes text as input.
    Returns a dictionary with:
    - style: one of Academic / Corporate / Creative / Casual
    - style_emoji: emoji for the style
    - style_description: what this style means
    - style_scores: scores for all 4 styles (so you can see how close it was)

    Example output:
    {
        "style": "Academic",
        "style_emoji": "🎓",
        "style_description": "Formal, structured writing typical of research or essays",
        "style_scores": {"Academic": 72, "Corporate": 45, "Creative": 20, "Casual": 10}
    }
    """
    text_lower = text.lower()
    words = text.split()
    sentences = [s.strip() for s in text.split(".") if s.strip()]

    # Calculate scores for each style (0-100)
    scores = {
        "Academic": _score_academic(text_lower, words, sentences),
        "Corporate": _score_corporate(text_lower, words, sentences),
        "Creative": _score_creative(text_lower, words, sentences),
        "Casual": _score_casual(text_lower, words, sentences)
    }

    # Normalize scores to be out of 100
    max_score = max(scores.values()) if max(scores.values()) > 0 else 1
    normalized = {k: round((v / max_score) * 100) for k, v in scores.items()}

    # Winner = highest score
    dominant_style = max(scores, key=scores.get)

    # Style metadata
    style_info = {
        "Academic": {
            "emoji": "🎓",
            "description": "Formal, structured writing typical of research papers or essays"
        },
        "Corporate": {
            "emoji": "💼",
            "description": "Professional, business-oriented writing with formal language"
        },
        "Creative": {
            "emoji": "✨",
            "description": "Expressive, imaginative writing with vivid language"
        },
        "Casual": {
            "emoji": "💬",
            "description": "Informal, conversational writing typical of everyday communication"
        }
    }

    info = style_info[dominant_style]

    return {
        "style": dominant_style,
        "style_emoji": info["emoji"],
        "style_description": info["description"],
        "style_scores": normalized
    }

def _score_academic(text, words, sentences):
    """Scores how academic the writing is."""
    score = 0

    academic_words = [
        "therefore", "furthermore", "consequently", "hypothesis",
        "methodology", "analysis", "conclusion", "research",
        "evidence", "significant", "demonstrate", "indicate",
        "study", "findings", "literature", "theoretical",
        "empirical", "framework", "paradigm", "discourse"
    ]
    score += sum(3 for w in academic_words if w in text)

    # Long sentences = academic
    avg_len = len(words) / max(len(sentences), 1)
    if avg_len > 20:
        score += 15
    elif avg_len > 15:
        score += 8

    # Passive voice markers
    passive_markers = ["was found", "were analyzed", "is considered", "has been"]
    score += sum(5 for p in passive_markers if p in text)

    return score

def _score_corporate(text, words, sentences):
    """Scores how corporate/business the writing is."""
    score = 0

    corporate_words = [
        "please", "kindly", "regards", "sincerely", "attached",
        "meeting", "deadline", "deliverable", "stakeholder",
        "leverage", "synergy", "bandwidth", "scalable", "agile",
        "roi", "kpi", "team", "project", "client", "proposal"
    ]
    score += sum(3 for w in corporate_words if w in text)

    # Formal greetings/closings
    if any(g in text for g in ["dear ", "hi team", "hello team", "best regards", "kind regards"]):
        score += 15

    return score

def _score_creative(text, words, sentences):
    """Scores how creative the writing is."""
    score = 0

    creative_words = [
        "whispered", "glowed", "shimmered", "felt", "breathed",
        "heart", "soul", "dream", "imagine", "suddenly",
        "beautiful", "darkness", "light", "journey", "story",
        "once upon", "moment", "laugh", "cry", "love"
    ]
    score += sum(3 for w in creative_words if w in text)

    # Varied sentence lengths = creative
    if sentences:
        lengths = [len(s.split()) for s in sentences]
        variance = max(lengths) - min(lengths) if lengths else 0
        if variance > 10:
            score += 10

    # Use of "I" = personal/creative writing
    if " i " in f" {text} " or text.startswith("i "):
        score += 8

    return score

def _score_casual(text, words, sentences):
    """Scores how casual/informal the writing is."""
    score = 0

    casual_words = [
        "hey", "yeah", "lol", "omg", "btw", "gonna", "wanna",
        "gotta", "cuz", "cause", "dunno", "kinda", "sorta",
        "stuff", "thing", "like", "pretty much", "totally",
        "awesome", "cool", "okay", "ok", "haha"
    ]
    score += sum(4 for w in casual_words if w in text)

    # Short sentences = casual
    avg_len = len(words) / max(len(sentences), 1)
    if avg_len < 10:
        score += 15

    # Contractions = casual
    contractions = ["don't", "can't", "won't", "it's", "i'm", "you're", "they're"]
    score += sum(3 for c in contractions if c in text)

    return score
