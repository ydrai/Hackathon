# session_state.py
import streamlit as st

def initialize_chat_history():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def add_message(role, message):
    st.session_state.chat_history.append((role, message))

def display_chat():
    for role, message in st.session_state.chat_history:
        st.chat_message(role.capitalize()).markdown(message)

def reset_chat():
    st.session_state.chat_history = []
    display_chat()
