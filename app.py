import streamlit as st
from modules import crm, voorraad, orders, facturatie, dashboard, planning

st.set_page_config(page_title="Voorraadbeheer Pro V15", layout="wide")

def main():
    st.sidebar.title("Navigatie")
    keuze = st.sidebar.radio("Ga naar module:", [
        "📚 CRM",
        "📦 Voorraad",
        "📝 Orders",
        "💶 Facturatie",
        "📊 Dashboard",
        "📅 Planning"
    ])

    if keuze == "📚 CRM":
        crm.app()
    elif keuze == "📦 Voorraad":
        voorraad.app()
    elif keuze == "📝 Orders":
        orders.app()
    elif keuze == "💶 Facturatie":
        facturatie.app()
    elif keuze == "📊 Dashboard":
        dashboard.app()
    elif keuze == "📅 Planning":
        planning.app()

if __name__ == "__main__":
    main()