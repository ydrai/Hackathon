# utils.py
import streamlit as st
from aws_client import AWSClient

def display_sidebar():
    st.sidebar.image('aws_icon.png', width=200)
    if st.sidebar.button('Reset Chat', use_container_width=True, key='reset_chat_button'):
        from session_state import reset_chat
        reset_chat()
        st.session_state.client = AWSClient()

def set_page_layout():
    st.set_page_config(page_title="Lex Chatbot", layout="wide")
