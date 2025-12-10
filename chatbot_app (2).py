import streamlit as st
import speech_recognition as sr
import random

# ---------------- Chatbot data with multiple responses ----------------
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
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
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
st.write("You can chat with the bot using text or upload a voice message (.wav).")

input_mode = st.radio("Choose input type:", ("Text", "Audio"))

if input_mode == "Text":
    user_input = st.text_input("Type your message here:")
    if user_input:
        response = chatbot_response(user_input)
        st.text_area("Chatbot Response", value=response, height=100)

elif input_mode == "Audio":
    audio_file = st.file_uploader("Upload a .wav audio file", type=["wav"])
    if audio_file:
        user_text = speech_to_text(audio_file)
        st.write("You said:", user_text)
        response = chatbot_response(user_text)
        st.text_area("Chatbot Response", value=response, height=100)

