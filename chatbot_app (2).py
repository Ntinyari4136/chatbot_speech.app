import streamlit as st
import random
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av
import numpy as np

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

# ---------------- Speech-to-text ----------------
recognizer = sr.Recognizer()

def speech_to_text_from_audio(audio_array, sample_rate):
    # Convert numpy audio array to audio file
    import tempfile
    import soundfile as sf
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, audio_array, sample_rate)
        with sr.AudioFile(f.name) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I could not understand the audio."
            except sr.RequestError:
                return "Could not request results; check your internet connection."

# ---------------- Streamlit WebRTC Audio Processor ----------------
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.user_text = None

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert to numpy
        audio_array = frame.to_ndarray()
        # Only process if not empty
        if audio_array.any():
            self.user_text = speech_to_text_from_audio(audio_array.T[0], frame.sample_rate)
        return frame

# ---------------- Streamlit app ----------------
st.title("Live Speech-Enabled Chatbot")
st.write("Talk to the bot using your microphone in real-time.")

# Start WebRTC for live audio
webrtc_ctx = webrtc_streamer(
    key="speech-chatbot",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True
)

if webrtc_ctx.audio_processor:
    user_text = webrtc_ctx.audio_processor.user_text
    if user_text:
        st.write("You said:", user_text)
        response = chatbot_response(user_text)
        st.text_area("Chatbot Response", value=response, height=100)

