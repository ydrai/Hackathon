import streamlit as st
from aws_interaction import AWSClient
import pandas as pd

def display_sidebar():
    """
    Displays the sidebar with an image and a reset button.
    """
    st.sidebar.image('TaxAuthority.png', width=200)
    if st.sidebar.button('איפוס שיחה', use_container_width=True, key='reset_chat_button'):
        from session_state import reset_chat
        reset_chat()
        st.session_state.client = AWSClient()

def set_page_layout():
    """
    Sets the layout of the Streamlit page.
    """
    st.set_page_config(page_title="החזר מסים", page_icon="TaxAuthority.png", layout="wide")

def clean_id_number(id_number):
    """
    Cleans and formats the ID number provided by the user.
    Extracts only digits and pads with leading zeros to make it 9 digits long.
    
    Args:
        id_number (str): The raw ID number input from the user.
    
    Returns:
        str: The cleaned and formatted ID number.
    """
    # Extract only digits
    digits_only = ''.join(filter(str.isdigit, id_number))
    # Pad with leading zeros to make it 9 digits long
    cleaned_id_number = digits_only.zfill(9)
    return cleaned_id_number

def load_hebrew_questions(file_path):
    df = pd.read_excel(file_path)
    questions = dict(zip(df['Question_English'], df['Question_Hebrew']))
    return questions
