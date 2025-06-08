import streamlit as st
from modules import crm, voorraad, orders, facturatie, planning, export_data

USERNAME = st.secrets["credentials"]["username"]
PASSWORD = st.secrets["credentials"]["password"]

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def login():
    st.sidebar.image('logo.png', use_container_width=True)
    st.title("🔐 Inloggen RENDER Platform")
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    if st.button("Inloggen"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.success("Inloggen gelukt!")
        else:
            st.error("Ongeldige inloggegevens.")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        st.sidebar.image('logo.png', use_container_width=True)
        st.sidebar.markdown("<h2 style='text-align: center; color: #333;'>🛠️ RENDER</h2>", unsafe_allow_html=True)
        page = st.sidebar.radio(
            "Navigatie",
            [
                "📚 CRM",
                "📦 Voorraad",
                "📝 Orders",
                "💶 Facturatie",
                "📅 Planning",
                "💾 Exporteer Data",
                "🚪 Uitloggen"
            ],
        )

        if page == "📚 CRM":
            crm.app()
        elif page == "📦 Voorraad":
            voorraad.app()
        elif page == "📝 Orders":
            orders.app()
        elif page == "💶 Facturatie":
            facturatie.app()
        elif page == "📅 Planning":
            planning.app()
        elif page == "💾 Exporteer Data":
            export_data.app()
        elif page == "🚪 Uitloggen":
            st.session_state['logged_in'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()