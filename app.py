# app.py
import streamlit as st
from aws_client import AWSClient
from session_state import initialize_chat_history, add_message, display_chat
from utils import set_page_layout, display_sidebar

def main():
    set_page_layout()
    display_sidebar()
    
    if 'client' not in st.session_state:
        st.session_state.client = AWSClient()
    
    st.sidebar.title("Session Details -----------")
    st.sidebar.write(f"Session ID: {str(st.session_state.client.session_id)[:15]}")

    initialize_chat_history()

    st.title(':grey[Claims - Tax Refund]')
    st.caption("If you paid taxes when you weren't supposed to, the chatbot will take care of everything 🙂")
    st.markdown('---')

    user_input = st.chat_input("Say something...")

    if user_input:
        try:
            add_message("user", user_input)
            bot_response = st.session_state.client.send_message(user_input)
            add_message("bot", bot_response)
        except Exception as e:
            st.write('Bot finished')
            st.error(f"An error occurred: {str(e)}")

    display_chat()

    # Handling file upload example
    if st.session_state.chat_history and st.session_state.chat_history[-1][1].startswith("Le double de"):
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)

if __name__ == "__main__":
    main()
