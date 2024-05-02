import streamlit as st
from boto3.session import Session
import json 
import sys

file_path = 'keys.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# Initialization of Lex client
lex_session = Session(
    aws_access_key_id     = data['Lex']['aws_access_key_id'],
    aws_secret_access_key = data['Lex']['aws_secret_access_key'],
    region_name           = data['Lex']['region_name'],
)
client = lex_session.client('lexv2-runtime')

def add_message(role, message):
    st.session_state.chat_history.append((role, message))

def display_chat():
    for role, message in st.session_state.chat_history:
        st.chat_message(role.capitalize()).markdown(message)

def send_to_lex(text):
    response = client.recognize_text(
        botId      = data['Lex']['bot_id'],
        botAliasId = data['Lex']['bot_alias_id'],
        localeId   = data['Lex']['locale_id'],
        sessionId  = "session3",
        text       = text
    )
    return response['messages'][0]['content']

# Streamlit page configuration
st.set_page_config(page_title="Lex Chatbot", layout="wide")

# Sidebar with image and reset button
st.sidebar.image('aws_icon.png', width=200)
if st.sidebar.button('Reset Chat', use_container_width=True):
    st.session_state.chat_history = []
    display_chat()

# Initialize chat history if not already present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title(':grey[Claims - Tax Refund]')
st.caption("If you paid taxes when you weren't supposed to, the chatbot will take care of everything 🙂")
st.markdown('---')

user_input = st.chat_input("Say something...")

if user_input:
    try:
        add_message("user", user_input)
        bot_response = send_to_lex(user_input)
        add_message("bot", bot_response)
    except Exception as e:
        st.write('Bot finished')
        sys.exit()

display_chat()

if st.session_state.chat_history and st.session_state.chat_history[-1][1].startswith("Le double de"):
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(type(bytes_data))
