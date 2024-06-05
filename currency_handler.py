import streamlit as st
import pandas as pd
from session_state import add_message
from aws_interaction import send_lex_message

def handle_currency_selection():
    """
    Displays a dropdown menu with currency options when prompted by the bot.
    """
    text_to_find = "בקשר לסכום שרשמת לפני, באיזה סוג מטבע מדובר?"
    if st.session_state.get('chat_history') and st.session_state['chat_history'][-1][0] == 'בוט' and text_to_find in st.session_state['chat_history'][-1][1]:
        currencies_df = pd.read_csv("combined_currencies_from_lex.csv")
        currency_options = [f"{row['Codes']} - {row['Symbol']}" for _, row in currencies_df.iterrows()]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_currency = st.selectbox("נא לבחור מטבע:", currency_options)
            selected_symbol = selected_currency.split(' - ')[-1]
            selected_code = selected_currency.split(' - ')[0]
            st.write(f"מטבע שנבחר: {selected_symbol}")
            st.session_state.selected_currency_symbol = selected_symbol
            if st.button("אשר/י מטבע"):
                try:
                    add_message("משתמש", f'{selected_code} - {selected_symbol}')
                    bot_response = st.session_state.client.send_lex_message(selected_code)
                    # Remplacer les variables en anglais par leur équivalent en hébreu
                    bot_response_hebrew = bot_response
                    bot_response_hebrew = bot_response_hebrew.replace("To summarize, your name is", "לסיכום, שם שלך הינו")
                    bot_response_hebrew = bot_response_hebrew.replace(", your ID number is", ", מספר ת.ז שלך הינו")
                    bot_response_hebrew = bot_response_hebrew.replace(", and the total amount is", " וסך הסכום ששילמת הינו ")
                    bot_response_hebrew = bot_response_hebrew.replace(". Is it this ?", ". האם הנתונים הללו נכונים?")
                    add_message("בוט", bot_response_hebrew)
                    st.session_state.awaiting_user_confirmation = True  # Mettre à jour l'état pour attendre la confirmation
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    add_message("בוט", "Bot finished")
    
    if st.session_state.get('awaiting_user_confirmation'):
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
        with col5:
            if st.button('כן ✅'):
                add_message("משתמש", "כן")
                st.session_state.awaiting_user_confirmation = False  # Réinitialiser l'état
                bot_response = send_lex_message("Yes")
                add_message("בוט", bot_response)
                st.experimental_rerun()
        with col6:  
            if st.button('לא ❌'):
                add_message("משתמש", "לא")
                st.session_state.awaiting_user_confirmation = False  # Réinitialiser l'état
                bot_response = send_lex_message("No")
                add_message("בוט", bot_response)
                st.experimental_rerun()
