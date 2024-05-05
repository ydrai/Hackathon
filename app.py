import streamlit as st
from aws_client import AWSClient
from session_state import initialize_chat_history, add_message, display_chat
from utils import set_page_layout, display_sidebar
import base64
import time

def create_client():
    """
    Creates and stores an AWSClient instance in the session state if it doesn't already exist.
    This function ensures that a client instance is available throughout the app's session.
    """
    if 'client' not in st.session_state:
        st.session_state['client'] = AWSClient()

def setup_sidebar():
    """
    Sets up the sidebar in the Streamlit interface with session details.
    It displays the session ID for the current user's interaction session.
    """
    st.sidebar.title("Session Details")
    session_id = str(st.session_state.client.session_id)[:15]
    st.sidebar.write(f"Session ID: {session_id}")

def handle_user_input():
    """
    Handles user input from the chat interface.
    It sends the user's input to the AWS Lex service using the client and displays the response.
    Errors are caught and displayed in the interface.
    """
    user_input = st.chat_input("Say something...")
    if user_input:
        add_message("user", user_input)
        try:
            bot_response = st.session_state.client.send_lex_message(user_input)
            add_message("bot", bot_response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            add_message("bot", "Bot finished")

def upload_section():
    """
    Manages the file upload section, allowing users to upload files when prompted by the chatbot.
    It handles file uploads and displays the filename after successful upload.
    """
    def convert_uploaded_file_to_base64(uploaded_file):
        """
        Converts a Streamlit UploadedFile object to a Base64 string.
        """
        uploaded_file.seek(0)  # Reset file pointer to the start
        file_data = uploaded_file.read()
        return base64.b64encode(file_data).decode('utf-8')
    
    def display_progress_bar():
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.03)
            progress_bar.progress(percent_complete + 1)

        st.success('Full loading')
    
    text_to_find = "Le double de"
    bot_message_found = any(
        speaker == 'bot' and message.startswith(text_to_find)
        for speaker, message in st.session_state.get('chat_history', [])
    )

    if bot_message_found:
        uploaded_file = st.file_uploader("Upload an image...", type=["pdf", "jpg", "jpeg", "png", "tif", "tiff"])
        if uploaded_file is not None:
            base64_string = convert_uploaded_file_to_base64(uploaded_file)
            
            # Pose the question
            question = "Do you confirm the information entered?"
            
            # Add a neutral default option
            response = st.selectbox(question, ['Select an option', 'No ❌', 'Yes ✅'], index=0)

            # Ensure the user makes a valid selection
            if response == 'Select an option':
                st.write("Please make a selection.")
            
            elif 'Yes' in response:
                st.write("You have confirmed the information.")
                display_progress_bar()
                st.session_state['client'] = AWSClient(service_name='lambda')
                entity_extraction = st.session_state.client.invoke_lambda('keyvalue_extraction', f'{{"image": "{base64_string}"}}')
                st.json(entity_extraction)

            else:
                st.write("You have not confirmed the information.")

def main():
    """
    Main function that serves as the entry point of the Streamlit application.
    It orchestrates the layout setup, sidebar setup, chat initialization, and other UI components.
    """
    set_page_layout()  # Set the overall page layout settings
    display_sidebar()  # Display static elements in the sidebar
    create_client()  # Ensure an AWS client is created and stored
    setup_sidebar()  # Set up dynamic elements in the sidebar
    initialize_chat_history()  # Initialize chat history for new sessions
    
    st.title(':grey[Claims - Tax Refund]')
    st.caption("If you paid taxes when you weren't supposed to, the chatbot will take care of everything 🙂")
    st.markdown('---')

    handle_user_input()  # Handle incoming user messages and responses
    display_chat()  # Display the chat history and interactions
    upload_section()  # Manage file uploads if prompted by the bot

if __name__ == "__main__":
    main()

