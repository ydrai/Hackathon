import streamlit as st
import base64
import time
from aws_interaction import invoke_lambda, AWSClient
from session_state import add_message

def handle_file_upload():
    """
    Manages the file upload section, allowing users to upload files when prompted by the chatbot.
    It handles file uploads and displays the filename after successful upload.
    """
    def convert_uploaded_file_to_base64(uploaded_file):
        """
        Converts a Streamlit UploadedFile object to a Base64 string.
        """
        uploaded_file.seek(0)
        file_data = uploaded_file.read()
        return base64.b64encode(file_data).decode('utf-8')

    def display_progress_bar():
        """
        Displays a progress bar during the loading process.
        """
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.success('הטעינה הושלמה, אנא המתן מספר שניות...')

    text_to_find = "נא להעלות את המסמך..."
    bot_message_found = any(
        speaker == 'בוט' and message.startswith(text_to_find)
        for speaker, message in st.session_state.get('chat_history', [])
    )

    if bot_message_found:
        st.session_state.user_data = extract_user_data(st.session_state.chat_history)
        uploaded_file = st.file_uploader("העלת תמונה...", type=["pdf", "jpg", "jpeg", "png", "tif", "tiff"])
        
        if uploaded_file is not None:
            base64_string = convert_uploaded_file_to_base64(uploaded_file)
            st.markdown('---')
            col1, col2 = st.columns(2)
            with col1:
                question = "האם אתה מאשר את המידע שהוזן?"
                response = st.selectbox(question, ['בחר/י אפשרות', 'לא ❌', 'כן ✅'], index=0)
            
            if response == 'בחר/י אפשרות':
                st.write("אנא בצע/י בחירה.")
            elif 'כן' in response:
                st.write("אישרת את המידע.")
                display_progress_bar()
                st.session_state['client'] = AWSClient(service_name='lambda')
                entity_extraction = invoke_lambda('keyvalue_extraction', f'{{"image": "{base64_string}"}}')
                st.json(entity_extraction)
            else:
                st.write("לא אישרת את המידע.")
                st.text(extract_user_data(st.session_state.chat_history))

def extract_user_data(chat_history):
    """
    Extracts user data from the chat history.
    """
    user_data = {
        "first_name": '',
        "last_name": '',
        "id_number": '',
        "total_value": '',
        "currency": ''
    }
    for i in range(len(chat_history) - 1):
        if chat_history[i][0] == 'בוט':
            if "מהו שם פרטי שלך?" in chat_history[i][1]:
                user_data["first_name"] = chat_history[i + 1][1]
            elif "מהו שם משפחה שלך?" in chat_history[i][1]:
                user_data["last_name"] = chat_history[i + 1][1]
            elif "מהו מספר תעודת זהות שלך?" in chat_history[i][1]:
                user_data["id_number"] = chat_history[i + 1][1]
            elif "מהו הסכום הכולל של כל המוצרים שקנית (ללא מטבע)?" in chat_history[i][1]:
                user_data["total_value"] = chat_history[i + 1][1]
            elif "בקשר לסכום שרשמת לפני, באיזה סוג מטבע מדובר?" in chat_history[i][1]:
                user_data["currency"] = chat_history[i + 1][1]

    return user_data
