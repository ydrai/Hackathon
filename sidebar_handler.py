import streamlit as st
from session_state import add_message
from aws_interaction import send_lex_message

def setup_sidebar():
    """
    Sets up the sidebar in the Streamlit interface with session details.
    It displays the session ID for the current user's interaction session.
    """
    # st.sidebar.title("פרטי שיחה")
    st.sidebar.markdown('<div style="direction: rtl; text-align: right;"><h1 style="color: grey;">פרטי שיחה</h1></div>', unsafe_allow_html=True)
    session_id = str(st.session_state.client.session_id)[:15]
    # st.sidebar.write(f"מזהה שיחה: {session_id}")
    st.sidebar.write(f'<div style="direction: rtl; text-align: right;">מזהה שיחה: {session_id}</div>', unsafe_allow_html=True)


def restart_chat():
    """
    Displays a confirmation button to restart the chat if the last bot message is "Ok, let's start again...".
    """
    text_to_find = "אין בעיה, נתחיל שוב..."
    if st.session_state.get('chat_history') and st.session_state['chat_history'][-1][0] == 'בוט' and text_to_find in st.session_state['chat_history'][-1][1]:
        if st.button("אוקיי ?"):
            try:
                add_message("משתמש", "אוקיי")
                bot_response = send_lex_message("Ok")
                add_message("בוט", bot_response)
                st.experimental_rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                add_message("בוט", "Bot finished")
