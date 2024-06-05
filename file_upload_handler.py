import streamlit as st
import base64
import time
from aws_interaction import start_step_function, AWSClient
from session_state import add_message
from chat_handler import display_chat
from PIL import Image
import io

def handle_file_upload():
    """
    Manages the file upload section, allowing users to upload files when prompted by the chatbot.
    It handles file uploads and displays the filename after successful upload.
    """
    def convert_uploaded_file_to_base64(file_data):
        """
        Converts a file data to a Base64 string.
        """
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

    def resize_image(image_data, max_size=(1024, 1024)):
        """
        Resizes an image to ensure it meets the size constraints.
        """
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGBA')

        image.thumbnail(max_size, Image.ANTIALIAS)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    
    def resize_image(image_data, max_size=(1024, 1024)):
        """
        Resizes an image to ensure it meets the size constraints.
        """
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGBA')
        image.thumbnail(max_size)
        buffer = io.BytesIO()
        # image.save(buffer, format="JPEG")
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    
    text_to_find = "נא להעלות את המסמך..."
    bot_message_found = any(
        speaker == 'בוט' and message.startswith(text_to_find)
        for speaker, message in st.session_state.get('chat_history', [])
    )

    if 'confirm_clicked' not in st.session_state:
        st.session_state.confirm_clicked = False

    if bot_message_found and not st.session_state.confirm_clicked:
        st.session_state.user_data = extract_user_data(st.session_state.chat_history)
        uploaded_file = st.file_uploader("העלת תמונה...", type=["pdf", "jpg", "jpeg", "png", "tif", "tiff"])
        
        if uploaded_file is not None:
            try:
                file_data = uploaded_file.read()
                base64_string = convert_uploaded_file_to_base64(file_data)
                
                # Check size after base64 encoding
                if len(base64_string) > 262144:
                    st.warning('גודל הקובץ גדול מדי. מנסים לדחוס את התמונה...')
                    time.sleep(3)
                    file_data = resize_image(file_data)
                    base64_string = convert_uploaded_file_to_base64(file_data)
                    if len(base64_string) > 262144:
                        st.error("לא ניתן לדחוס את התמונה לגודל המתאים")
                        return
                    else:
                        st.info('התמונה נדחסה')
                        time.sleep(2)
                
                st.session_state.uploaded_file = base64_string  # Stocker l'image encodée en base64 dans l'état de session
                st.markdown('---')
                st.write("האם אתה מאשר את המידע שהוזן?")

                # Créez les colonnes pour les boutons
                col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
                with col5:
                    confirm = st.button('כן ✅')
                with col6:
                    deny = st.button('לא ❌')

                if confirm:
                    st.session_state.confirm_clicked = True  # Désactiver les boutons après clic
                    add_message("משתמש", "כן")
                    st.write("אישרת את המידע.")
                    display_progress_bar()
                    
                    st.session_state['client'] = AWSClient(service_name='stepfunctions')
                    try:
                        result = start_step_function(st.secrets.aws_credentials["state_machine_arn"], {"image": st.session_state.uploaded_file})

                        deal_text_generation = result[0]["deal_text_generation"]
                        dict_text_generated  = result[1]["dict_text_generated"]

                        add_message("בוט", deal_text_generation)
                        st.experimental_rerun()
                    except Exception as e:
                        st.session_state.confirm_clicked = False
                        st.session_state['uploaded_file'] = None
                        # add_message("בוט", "גודל של התמונה גדול מידי, נא לבחור בתמונה ששוקלת פחות.")
                        st.error("גודל של התמונה גדול מידי, נא לבחור בתמונה ששוקלת פחות.")
                        st.experimental_rerun()
                elif deny:
                    st.session_state.confirm_clicked = False  # Désactiver les boutons après clic
                    add_message("משתמש", "לא")
                    st.write("לא אישרת את המידע.")
                    st.experimental_rerun()
            except Exception as e:
                st.write(f"שגיאה: {str(e)}")
                st.session_state.uploaded_file = None  # Supprimer le fichier téléchargé
                st.experimental_rerun()

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
