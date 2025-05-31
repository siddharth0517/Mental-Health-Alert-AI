import streamlit as st
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mailimport streamlit as st
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import speech_recognition as sr
import tempfile
import os

# --- Streamlit Page Config ---
st.set_page_config(page_title="Mental Health Crisis Predictor", page_icon="🧠", layout="wide")

# --- Setup OpenRouter API ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# --- Email Alert Function ---
def send_alert_email(message):
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        email = Mail(
            from_email=st.secrets["ALERT_EMAIL_FROM"],
            to_emails=st.secrets["ALERT_EMAIL_TO"],
            subject="🚨 Mental Health Crisis Alert",
            html_content=f"<strong>{message}</strong>"
        )
        sg.send(email)
        st.success("🚨 Alert sent to trusted contact!")
    except Exception as e:
        st.error(f"❌ Failed to send alert: {e}")

# --- AI Analysis ---
def analyze_with_gemma(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-maverick:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a compassionate mental health assistant. "
                        "Analyze the user's message for signs of emotional distress, depression, or suicidal ideation. "
                        "Reply in the format:\n\n"
                        "Risk Level: [Low | Medium | High]\nExplanation: [short explanation of why you judged this risk level]"
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error from AI: {e}"

# --- Tabs ---
tab1, tab2 = st.tabs(["💬 User Analysis", "📊 Therapist Dashboard"])

# ============================
# 💬 User Analysis Tab
# ============================
with tab1:
    st.markdown("## 🧠 Mental Health Crisis Predictor")
    st.markdown("Analyze user input for signs of emotional or mental distress.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # --- Text Input ---
    with col1:
        st.markdown("### 📝 Text Analysis")
        text_input = st.text_area("Enter a message (e.g., chat or social media)", height=150)
        
        if st.button("🔍 Analyze Text"):
            if text_input.strip():
                with st.spinner("Analyzing..."):
                    result = analyze_with_gemma(text_input)
                    st.success("✅ Analysis Complete")
                    st.markdown(f"**AI Result:**\n```{result}```")

                    if "High" in result:
                        send_alert_email(
                            f"High-risk message detected:\n\n{text_input}\n\nResponse:\n{result}"
                        )
            else:
                st.warning("⚠️ Please enter a message before analyzing.")

    # --- Voice Input ---
    with col2:
        st.markdown("### 🎤 Voice Analysis")
        audio_file = st.file_uploader("Upload a voice message", type=["wav", "mp3"])

        if audio_file is not None:
            st.audio(audio_file, format="audio/wav")
            recognizer = sr.Recognizer()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_filename = tmp_file.name

            with sr.AudioFile(tmp_filename) as source:
                audio_data = recognizer.record(source)

            try:
                transcribed_text = recognizer.recognize_google(audio_data)
                st.markdown(f"🔊 **Transcribed Text:**\n> _{transcribed_text}_")

                with st.spinner("Analyzing voice content..."):
                    voice_result = analyze_with_gemma(transcribed_text)
                    st.success("✅ Analysis Complete")
                    st.markdown(f"**AI Result:**\n```{voice_result}```")

                    if "High" in voice_result:
                        send_alert_email(
                            f"High-risk voice detected:\n\n{transcribed_text}\n\nResponse:\n{voice_result}"
                        )

            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError as e:
                st.error(f"❌ Google Speech API Error: {e}")
            finally:
                os.remove(tmp_filename)

# ============================
# 📊 Therapist Dashboard Tab
# ============================
with tab2:
    st.markdown("## 📊 Therapist & Caregiver Dashboard")
    st.markdown("Track previous assessments and flagged alerts below.")

    st.markdown("---")

    # Dummy logs for demo
    example_logs = [
        {"type": "Text", "input": "I don't want to live anymore.", "risk": "High"},
        {"type": "Voice", "input": "I'm tired of trying every day.", "risk": "Medium"},
        {"type": "Text", "input": "Today was actually okay.", "risk": "Low"},
    ]

    color_map = {
        "High": "#FFCCCC",
        "Medium": "#FFE5B4",
        "Low": "#D4EDDA"
    }

    emoji_map = {
        "High": "🔴",
        "Medium": "🟠",
        "Low": "🟢"
    }

    for log in example_logs:
        bg_color = color_map[log["risk"]]
        emoji = emoji_map[log["risk"]]

        st.markdown(
            f"""
            <div style="background-color:{bg_color};padding:10px;border-radius:10px;margin-bottom:10px">
                <strong>Type:</strong> {log['type']}<br>
                <strong>Risk Level:</strong> {emoji} {log['risk']}<br>
                <strong>Content:</strong> <em>{log['input']}</em>
            </div>
            """,
            unsafe_allow_html=True
        )

import speech_recognition as sr
import tempfile
import os

# --- Setup OpenRouter API ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# --- Email Alert Function ---
def send_alert_email(message):
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        email = Mail(
            from_email=st.secrets["ALERT_EMAIL_FROM"],
            to_emails=st.secrets["ALERT_EMAIL_TO"],
            subject="🚨 Mental Health Crisis Alert",
            html_content=f"<strong>{message}</strong>"
        )
        sg.send(email)
        st.success("🚨 Alert sent to trusted contact!")
    except Exception as e:
        st.error(f"❌ Failed to send alert: {e}")

# --- Gemma AI Analysis ---
def analyze_with_gemma(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-maverick:free",  # ✅ FIXED: Correct model name
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a compassionate mental health assistant. "
                        "Analyze the user's message for signs of emotional distress, depression, or suicidal ideation. "
                        "Reply in the format:\n\n"
                        "Risk Level: [Low | Medium | High]\nExplanation: [short explanation of why you judged this risk level]"
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error from Gemma API: {e}"

# --- Streamlit Tabs ---
tab1, tab2 = st.tabs(["💬 User Analysis", "📊 Therapist Dashboard"])

# ===========================
# 💬 User Analysis Tab
# ===========================
with tab1:
    st.title("🧠 Mental Health Crisis Predictor")

    st.subheader("Text Input")
    text_input = st.text_area("Enter a message (e.g., chat or social media)", height=150)
    
    if st.button("🔍 Analyze Text"):
        if text_input.strip():
            with st.spinner("Analyzing..."):
                result = analyze_with_gemma(text_input)
                st.write("**AI Result:**", result)

                if "High" in result:
                    send_alert_email(
                        f"High-risk message detected:\n\n{text_input}\n\nResponse:\n{result}"
                    )
        else:
            st.warning("Please enter a message before analyzing.")

    st.subheader("Voice Input")
    audio_file = st.file_uploader("Upload a voice message", type=["wav", "mp3"])

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_filename = tmp_file.name

        with sr.AudioFile(tmp_filename) as source:
            audio_data = recognizer.record(source)

        try:
            transcribed_text = recognizer.recognize_google(audio_data)
            st.write("🔊 Transcribed Text:", transcribed_text)

            with st.spinner("Analyzing voice content..."):
                voice_result = analyze_with_gemma(transcribed_text)
                st.write("**AI Result:**", voice_result)

                if "High" in voice_result:
                    send_alert_email(
                        f"High-risk voice detected:\n\n{transcribed_text}\n\nResponse:\n{voice_result}"
                    )

        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ Error from Google Speech API: {e}")
        finally:
            os.remove(tmp_filename)

# ===========================
# 📊 Therapist Dashboard Tab
# ===========================
with tab2:
    st.title("📊 Therapist & Caregiver Dashboard")
    st.markdown("View summarized assessments, alerts, and flagged content.")

    # 🔧 For demo: use dummy data — replace with real logs in production
    example_logs = [
        {"type": "Text", "input": "I don't want to live anymore.", "risk": "High"},
        {"type": "Voice", "input": "I'm tired of trying every day.", "risk": "Medium"},
        {"type": "Text", "input": "Today was actually okay.", "risk": "Low"},
    ]

    for log in example_logs:
        emoji = {
            "High": "🔴",
            "Medium": "🟠",
            "Low": "🟢"
        }[log["risk"]]

        st.markdown(f"""
        **Type**: {log['type']}  
        **Risk Level**: {emoji} **{log['risk']}**  
        **Content**: _{log['input']}_  
        ---
        """)
