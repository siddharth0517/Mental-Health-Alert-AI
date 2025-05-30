import streamlit as st
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import speech_recognition as sr
import tempfile

# --- Setup OpenRouter API ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# --- Email Alert Function ---
def send_alert_email(message):
    sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
    email = Mail(
        from_email=st.secrets["ALERT_EMAIL_FROM"],
        to_emails=st.secrets["ALERT_EMAIL_TO"],
        subject="🚨 Mental Health Crisis Alert",
        html_content=f"<strong>{message}</strong>"
    )
    try:
        sg.send(email)
        st.success("🚨 Alert sent to trusted contact!")
    except Exception as e:
        st.error(f"Failed to send alert: {e}")

# --- Gemma AI Analysis ---
def analyze_with_gemma(prompt):
    response = client.chat.completions.create(
        model="google/gemma-3n-e4b-it:free",
        messages=[
            {"role": "system", "content": "You are a mental health assistant. Analyze input for signs of distress. Respond with risk level (Low, Medium, High) and a brief explanation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- Streamlit Tabs ---
tab1, tab2 = st.tabs(["💬 User Analysis", "📊 Therapist Dashboard"])

# ===========================
# 💬 User Analysis Tab
# ===========================
with tab1:
    st.title("🧠 Mental Health Crisis Predictor")

    st.subheader("Text Input")
    text_input = st.text_area("Enter a message (e.g., chat or social media)", height=150)
    
    if st.button("Analyze Text"):
        with st.spinner("Analyzing..."):
            result = analyze_with_gemma(text_input)
            st.write("**AI Result:**", result)

            if "High" in result:
                send_alert_email(f"High-risk message detected:\n\n{text_input}\n\nResponse:\n{result}")

    st.subheader("Voice Input")
    audio_file = st.file_uploader("Upload a voice message", type=["wav", "mp3"])
    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")
        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
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
                        send_alert_email(f"High-risk voice detected:\n\n{transcribed_text}\n\nResponse:\n{voice_result}")

            except sr.UnknownValueError:
                st.error("Could not understand audio.")

# ===========================
# 📊 Therapist Dashboard Tab
# ===========================
with tab2:
    st.title("📊 Therapist & Caregiver Dashboard")
    st.markdown("View summarized assessments, alerts, and flagged content.")

    # For demo: use dummy data — replace with database logs in production
    example_logs = [
        {"type": "Text", "input": "I don't want to live anymore.", "risk": "High"},
        {"type": "Voice", "input": "I'm tired of trying every day.", "risk": "Medium"},
        {"type": "Text", "input": "Today was actually okay.", "risk": "Low"},
    ]

    for log in example_logs:
        st.markdown(f"""
        **Type**: {log['type']}  
        **Risk Level**: :{'red_circle:' if log['risk']=="High" else 'orange_circle:' if log['risk']=="Medium" else 'green_circle:'} **{log['risk']}**  
        **Content**: _{log['input']}_  
        ---
        """)

