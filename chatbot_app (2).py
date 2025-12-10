import streamlit as st
import speech_recognition as sr
import random
import tempfile

# ---------------- Chatbot data ----------------
raw_data = {
    "hello": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! How’s it going?"
    ],
    "how are you": [
        "I am fine, thank you! How about you?",
        "Doing well! How are you?",
        "I’m great, thanks for asking!"
    ],
    "help": [
        "Sure! Tell me what you need help with.",
        "I am here to assist. What do you need?",
        "Absolutely! How can I help you today?"
    ],
    "default": [
        "I am sorry, I don't understand.",
        "Can you please rephrase that?",
        "Hmm, I am not sure I got that."
    ]
}

# ---------------- Chatbot response function ----------------
def chatbot_response(user_input):
    user_input_lower = user_input.lower()
    for key in raw_data.keys():
        if key in user_input_lower:
            return random.choice(raw_data[key])
    return random.choice(raw_data["default"])

# ---------------- Speech-to-text function ----------------
def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name

    with sr.AudioFile(tmp_file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Could not request results; check your internet connection."

# ---------------- Streamlit app ----------------
st.title("Speech-Enabled Chatbot")
st.write("You can chat with the bot using text or speak directly through your microphone.")

input_mode = st.radio("Choose input type:", ("Text", "Microphone"))

# -------- Text input --------
if input_mode == "Text":
    user_input = st.text_input("Type your message here:")
    if user_input:
        response = chatbot_response(user_input)
        st.text_area("Chatbot Response", value=response, height=100)

# -------- Microphone input --------
elif input_mode == "Microphone":
    st.write("Click 'Start Recording', speak, then click 'Stop Recording'")
    audio_bytes = st.audio_input("Record your voice:", type="wav")
    if audio_bytes:
        user_text = speech_to_text(audio_bytes)
        st.write("You said:", user_text)
        response = chatbot_response(user_text)
        st.text_area("Chatbot Response", value=response, height=100)

