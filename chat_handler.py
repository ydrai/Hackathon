import streamlit as st
from session_state import add_message
from aws_interaction import send_lex_message
from utils import clean_id_number

def handle_user_input():
    """
    Handles user input from the chat interface.
    Sends the user's input to the AWS Lex service using the client and displays the response.
    Ensures the user enters an ID number before proceeding.
    """
    if not st.session_state.chat_blocked:
        user_input = st.chat_input("Say something...")
        if user_input:
            if st.session_state.get('awaiting_id_number', False):
                cleaned_id = clean_id_number(user_input)
                add_message("משתמש", cleaned_id)
                st.session_state.awaiting_id_number = False
                try:
                    bot_response = send_lex_message(cleaned_id)
                    add_message("בוט", bot_response)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    add_message("בוט", "Bot finished")
            else:
                add_message("משתמש", user_input)
                try:
                    if not st.session_state.first_response_analyzed:
                        first_response_analysis(user_input)
                        st.session_state.first_response_analyzed = True
                    else:
                        bot_response = send_lex_message(user_input)
                        if "מהו מספר תעודת זהות שלך?" in bot_response:
                            st.session_state.awaiting_id_number = True
                        add_message("בוט", bot_response)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    add_message("בוט", "Bot finished")

def first_response_analysis(user_input):
    """
    Analyzes the first response from the user.
    If the response starts with "y" or "o", it sends "Yes" to Amazon Lex.
    Otherwise, it ends the conversation.
    """
    if user_input.lower().startswith("ל"):
        add_message("בוט", 'סבבה, אם תצטרך עוד משהו אל תתלבט.   \nעל מנת להתחיל מחדש תלחץ על כפתור "איפוס שיחה"')
        st.session_state.chat_blocked = True
        st.experimental_rerun()
    else:
        try:
            bot_response = send_lex_message("Yes")
            if "מהו מספר תעודת זהות שלך?" in bot_response:
                st.session_state.awaiting_id_number = True
            add_message("בוט", bot_response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            add_message("בוט", "Bot finished")

def display_chat():
    """
    Displays the chat history in a visually appealing way in the Streamlit interface.
    """
    # Utilisation d'un conteneur pour organiser le chat
    chat_container = st.container()
    
    # Boucle sur chaque message du chat
    for role, message in st.session_state.chat_history:
        # Styles différents selon le rôle
        if role == "בוט":
            background_color = "#f0f0f0"
            text_color = "#333333"
            align = "left"
            role_text_style = "font-size: larger;"
            bubble_style = "border: 2px solid #999999; border-radius: 10px; padding: 10px; margin: 5px; position: relative;"
            pointer_style = "content: ''; position: absolute; top: 50%; right: 100%; border: 10px solid transparent; border-right-color: #999999;"
        else:
            background_color = "#d9edf7"
            text_color = "#31708f"
            align = "right"
            role_text_style = "font-size: larger;"
            bubble_style = "border: 2px solid #5bc0de; border-radius: 10px; padding: 10px; margin: 5px; position: relative;"
            pointer_style = "content: ''; position: absolute; top: 50%; left: 100%; border: 10px solid transparent; border-left-color: #5bc0de;"

        # Affichage du message avec le rôle et le message
        with chat_container:
            st.markdown(
                f'<div style="background-color: {background_color}; {bubble_style} text-align: {align}; direction: rtl; color: {text_color};">{message}<span style="{pointer_style}"></span></div>',
                unsafe_allow_html=True
            )