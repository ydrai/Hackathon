import streamlit as st
from chat_handler import handle_user_input, display_chat
from sidebar_handler import setup_sidebar, restart_chat
from file_upload_handler import handle_file_upload
from currency_handler import handle_currency_selection
from aws_interaction import create_client
from utils import set_page_layout, display_sidebar, load_hebrew_questions
from session_state import initialize_chat_history

def main():
    """
    Main function that serves as the entry point of the Streamlit application.
    It orchestrates the layout setup, sidebar setup, chat initialization, and other UI components.
    """
    set_page_layout()
    display_sidebar()
    create_client()
    
    setup_sidebar()
    initialize_chat_history()

    st.markdown('<div style="direction: rtl; text-align: right;"><h1 style="color: grey;">תביעות - החזר מיסים</h1></div>', unsafe_allow_html=True)
    st.markdown('<div style="direction: rtl; text-align: right;">אם שילמת מיסים שלא היית אמור לשלם עליהם, נדאג להחזר 🙂</div>', unsafe_allow_html=True)
    st.markdown('---')
        
    handle_user_input()
    display_chat()    
    handle_currency_selection()
    handle_file_upload()
    restart_chat()

if __name__ == "__main__":
    main()

# import streamlit as st
# import base64
# def convert_uploaded_file_to_base64(uploaded_file):
#         """
#         Converts a Streamlit UploadedFile object to a Base64 string.
#         """
#         uploaded_file.seek(0)
#         file_data = uploaded_file.read()
#         return base64.b64encode(file_data).decode('utf-8')

# uploaded_file = st.file_uploader("העלת תמונה...", type=["pdf", "jpg", "jpeg", "png", "tif", "tiff"])

# if uploaded_file is not None:
#     base64_string = convert_uploaded_file_to_base64(uploaded_file)
#     st.text(base64_string)