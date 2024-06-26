import streamlit as st
from utils import load_hebrew_questions

def initialize_chat_history():
    """
    Initializes the session state variables.
    """
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state['chat_history']:
        add_message("בוט", "היי, אני הבוט שיעזור לך לקבל חזרה את המיסים המיותרים ששילמת עבור ההזמנות שלך. בשביל זה אני אשאל אותך כמה שאלות, בסדר?")

    if 'first_response_analyzed' not in st.session_state:
        st.session_state.first_response_analyzed = False

    if 'chat_blocked' not in st.session_state:
        st.session_state.chat_blocked = False

    if 'restart_triggered' not in st.session_state:
        st.session_state.restart_triggered = False

    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    if 'awaiting_id_number' not in st.session_state:
        st.session_state.awaiting_id_number = False

    if 'hebrew_questions' not in st.session_state:
        hebrew_questions = load_hebrew_questions("Hebrew_Questions.xlsx")
        st.session_state.hebrew_questions = hebrew_questions

    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ''

    if 'selected_currency' not in st.session_state:
        st.session_state.selected_currency = 'USD'

    if 'client' not in st.session_state:
        st.session_state.client = None

    if 'confirm_clicked' not in st.session_state:
        st.session_state.confirm_clicked = False

    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = False

def add_message(role, message):
    """
    Adds a message to the chat history in the session state.
    
    Args:
        role (str): The role of the message sender, either 'bot' or 'user'.
        message (str): The message content.
    """
    st.session_state.chat_history.append((role, message))

def display_chat():
    """
    Displays the chat history in the Streamlit interface.
    """
    for role, message in st.session_state.chat_history:
        st.chat_message(role.capitalize()).markdown(message)

def reset_chat():
    """
    Resets all session state variables.
    """
    st.session_state.chat_history = []
    st.session_state.first_response_analyzed = False
    st.session_state.chat_blocked = False
    st.session_state.restart_triggered = False
    st.session_state.user_data = {}
    st.session_state.awaiting_id_number = False
    st.session_state.hebrew_questions = load_hebrew_questions("Hebrew_Questions.xlsx")
    st.session_state.chat_input = ''
    st.session_state.selected_currency = 'USD'
    st.session_state.client = None
    st.session_state.confirm_clicked = False
    st.session_state.generated_text = False
    display_chat()
