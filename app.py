
import streamlit as st
import sys
import os

# Tell Python where to find our modules folder
sys.path.append(os.path.dirname(__file__))

from modules.ai_detector import detect_ai
from modules.emotion_analyzer import analyze_emotion
from modules.style_tagger import tag_writing_style

# PAGE SETUP

st.set_page_config(page_title="AI Writing Style Detector", page_icon="🕵️")

# TITLE

st.title("🕵️ AI Writing Style Detector")
st.write("Paste any text below and find out if it's AI or Human written, its emotion, and writing style.")

st.divider()

# SAMPLE BUTTONS

st.write("**Try a sample text:**")

col1, col2, col3 = st.columns(3)

AI_SAMPLE = """The implementation of artificial intelligence in modern healthcare systems represents a paradigm shift in diagnostic methodologies. Furthermore, the integration of machine learning algorithms enables clinicians to identify pathological patterns with unprecedented accuracy. Consequently, patient outcomes are significantly improved through data-driven decision-making frameworks."""

HUMAN_SAMPLE = """okay so i've been trying to figure out this whole gym thing for like 3 months now lol. honestly i keep telling myself i'll start on monday but then monday comes and i'm like... nah. my friend keeps saying i just need to find something i actually enjoy doing. maybe she's right? idk, i'll probably try that yoga class this weekend."""

CREATIVE_SAMPLE = """The old lighthouse stood at the edge of the world, its beam cutting through the darkness like a whispered promise. She had come here every summer as a child, chasing crabs through the tide pools while her grandmother hummed old songs that smelled of salt and memory."""

if col1.button("🤖 AI Sample"):
    st.session_state.sample_text = AI_SAMPLE

if col2.button("✍️ Human Sample"):
    st.session_state.sample_text = HUMAN_SAMPLE

if col3.button("✨ Creative Sample"):
    st.session_state.sample_text = CREATIVE_SAMPLE


# TEXT INPUT

default_text = st.session_state.get("sample_text", "")

user_text = st.text_area(
    "Paste your text here:",
    value=default_text,
    height=200,
    placeholder="Type or paste any text here... (minimum 10 words)"
)


# ANALYZE BUTTON

analyze_clicked = st.button("🔍 Analyze Text", type="primary", use_container_width=True)


# ANALYSIS — runs only when button is clicked

if analyze_clicked:

    # Check if text is empty
    if not user_text.strip():
        st.error("Please paste some text first!")

    # Check if text is too short
    elif len(user_text.split()) < 10:
        st.warning("Text is too short. Please enter at least 10 words.")

    else:
        # Show loading spinner while analyzing
        with st.spinner("Analyzing your text..."):
            ai_result        = detect_ai(user_text)
            emotion_result   = analyze_emotion(user_text)
            style_result     = tag_writing_style(user_text)

        st.success("Analysis complete!")
        st.divider()
        
        # SECTION 1: AI vs HUMAN
       
        st.header("🤖 AI vs Human Detection")

        st.write("**Verdict:**", ai_result["verdict"])
        st.write("**Confidence:**", ai_result["confidence"])

        col_ai, col_human = st.columns(2)

        with col_ai:
            st.metric("AI Probability", f"{ai_result['ai_score']}%")
            st.progress(ai_result["ai_score"] / 100)

        with col_human:
            st.metric("Human Probability", f"{ai_result['human_score']}%")
            st.progress(ai_result["human_score"] / 100)

        st.write("**Key Signals:**")
        for signal in ai_result["signals"]:
            st.write("-", signal)

        st.divider()

        # SECTION 2: EMOTION & TONE
   
        st.header("🎭 Emotion & Tone")

        st.write("**Dominant Emotion:**", emotion_result["emotion_emoji"], emotion_result["dominant_emotion"])
        st.write("**Tone:**", emotion_result["tone"])
        st.write("**Description:**", emotion_result["tone_description"])

        st.write("**All Emotion Scores:**")
        for emotion, score in emotion_result["emotion_scores"].items():
            st.write(f"{emotion}: {score}%")
            st.progress(score / 100)

        st.divider()

        # SECTION 3: WRITING STYLE
      
        st.header("🏷️ Writing Style")

        st.write("**Style:**", style_result["style_emoji"], style_result["style"])
        st.write("**Description:**", style_result["style_description"])

        st.write("**All Style Scores:**")
        for style, score in style_result["style_scores"].items():
            st.write(f"{style}: {score}%")
            st.progress(score / 100)

        st.divider()

        # SECTION 4: SUMMARY
        
        st.header("📊 Summary")

        st.write("| Category | Result |")
        st.write("|---|---|")
        st.write(f"| AI Detection | {ai_result['verdict']} ({ai_result['confidence']} confidence) |")
        st.write(f"| AI Probability | {ai_result['ai_score']}% |")
        st.write(f"| Human Probability | {ai_result['human_score']}% |")
        st.write(f"| Dominant Emotion | {emotion_result['emotion_emoji']} {emotion_result['dominant_emotion']} |")
        st.write(f"| Writing Tone | {emotion_result['tone']} |")
        st.write(f"| Writing Style | {style_result['style_emoji']} {style_result['style']} |")

# FOOTER

st.divider()
st.caption("AI Writing Style Detector | Built with Streamlit + HuggingFace")
