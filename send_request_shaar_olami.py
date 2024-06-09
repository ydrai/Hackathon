import streamlit as st
import time
from session_state import add_message

def send_request():
    if st.session_state.generated_text:
        # Créez les colonnes pour les boutons
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
        with col5:
            confirm = st.button('כן ✅')
        with col6:
            deny = st.button('לא ❌')

        if confirm:
            # Injecter du JavaScript pour afficher une alerte de confirmation
            st.success("ההודעה נשלחה בהצלחה והיא תטופל בהקדם האפשרי")
            time.sleep(5)
            
            add_message("משתמש", 'כן')
            add_message("בוט", 'פנייתך נשלחה ושיחה זו הסתיימה.')
            
            st.session_state.generated_text = False
            st.experimental_rerun()
        elif deny:
            st.info("ההודעה לא נשלחה")
            time.sleep(3)
            
            add_message("משתמש", 'לא')
            add_message("בוט", 'פנייתך לא נשלחה ושיחה זו הסתיימה.')

            st.session_state.generated_text = False
            st.experimental_rerun()

        

