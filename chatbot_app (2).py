
import streamlit as st
import nltk
import string
import speech_recognition as sr
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import os

nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('wordnet', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)

# Tell NLTK to look for data in this folder
nltk.data.path.append(nltk_data_path)

# ---------------- NLTK setup ----------------
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# ---------------- Chatbot data embedded directly ----------------
raw_data = """
Hello, how can I help you today?
I am a chatbot.
You can ask me questions about anything.
Feel free to talk to me.
I am here to assist you.
""".lower()

sent_tokens = [line.strip() for line in raw_data.split("\n") if line.strip()]

lemmer = WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    # Lowercase, remove punctuation, split by spaces
    return [word for word in text.lower().translate(remove_punct_dict).split() if word]


# ---------------- Chatbot response function ----------------
def chatbot_response(user_input):
    sent_tokens.append(user_input)
    
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = vals.argmax()
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-1]
    
    if req_tfidf == 0:
        robo_response = "I am sorry, I don't understand."
    else:
        robo_response = sent_tokens[idx]
    
    sent_tokens.pop()
    return robo_response

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
