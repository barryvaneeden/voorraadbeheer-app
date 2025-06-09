import streamlit as st
import json
import os

ORDERS_FILE = "data/orders_data.json"
CRM_FILE = "data/crm_data.json"
VOORRAAD_FILE = "data/voorraad_data.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def app():
    st.subheader("➕ Nieuwe order toevoegen")
    orders = load_data(ORDERS_FILE)
    klanten = load_data(CRM_FILE)
    producten = load_data(VOORRAAD_FILE)

    klantnamen = [klant["naam"] for klant in klanten]
    productnamen = [product["naam"] for product in producten]

    if not klanten or not producten:
        st.warning("Voeg eerst klanten en producten toe!")
        return

    with st.form("order_form", clear_on_submit=True):
        klant = st.selectbox("Selecteer klant", klantnamen)
        gekozen_producten = st.multiselect("Selecteer producten", productnamen)
        korting = st.number_input("Korting (%)", min_value=0.0, max_value=100.0, step=0.5)
        status = st.selectbox("Orderstatus", ["Nieuw", "In behandeling", "Afgerond"])

        submitted = st.form_submit_button("Toevoegen")

        if submitted:
            order = {
                "klant": klant,
                "producten": gekozen_producten,
                "korting": korting,
                "status": status
            }
            orders.append(order)
            save_data(ORDERS_FILE, orders)
            st.success(f"Order voor {klant} toegevoegd!")

    st.subheader("📋 Overzicht orders")
    if orders:
        for idx, order in enumerate(orders):
            st.write(f"**Klant:** {order['klant']}")
            st.write(f"Producten: {', '.join(order['producten'])}")
            st.write(f"Korting: {order['korting']}%")
            st.write(f"Status: {order['status']}")
    else:
        st.info("Nog geen orders toegevoegd.")