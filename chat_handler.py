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
        user_input = st.chat_input("תגיד/י משהו...")
        
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

    # Styles CSS pour une meilleure ambiance de chat
    st.markdown(
        """
        <style>
        .chat-bubble {
            border-radius: 20px;
            padding: 10px;
            margin: 10px 0;
            position: relative;
            max-width: 60%;
            display: inline-block;
            direction: rtl; /* Alignement du texte de droite à gauche */
        }
        .chat-bubble.bot {
            background-color: #f0f0f0;
            color: #333;
            border: 2px solid #999;
            text-align: right;
            margin-right: auto; /* Alignement des bulles à gauche */
        }
        .chat-bubble.user {
            background-color: #d9edf7;
            color: #31708f;
            border: 2px solid #5bc0de;
            text-align: right;
            margin-left: auto; /* Alignement des bulles à droite */
        }
        .chat-bubble::after {
            content: '';
            position: absolute;
            top: 50%;
            width: 0;
            height: 0;
            border: 10px solid transparent;
        }
        .chat-bubble.bot::after {
            border-right-color: #999;
            right: 100%;
            margin-top: -10px;
        }
        .chat-bubble.user::after {
            border-left-color: #5bc0de;
            left: 100%;
            margin-top: -10px;
        }
        .chat-message {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            direction: rtl; /* Alignement du texte de droite à gauche */
        }
        .chat-message.bot {
            justify-content: flex-start; /* Alignement des messages du bot à gauche */
        }
        .chat-message.user {
            justify-content: flex-end; /* Alignement des messages de l'utilisateur à droite */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Boucle sur chaque message du chat
    for role, message in st.session_state.chat_history:
        message_alignment = "bot" if role == "בוט" else "user"

        with chat_container:
            st.markdown(
                f"""
                <div class="chat-message {message_alignment}">
                    <div class="chat-bubble {message_alignment}">
                        {message}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )