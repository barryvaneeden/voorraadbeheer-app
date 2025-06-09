import streamlit as st
import json
import pandas as pd
import plotly.express as px
import os

ORDERS_FILE = "data/orders_data.json"
VOORRAAD_FILE = "data/voorraad_data.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def app():
    st.subheader("📊 Dashboard Overzicht")
    orders = load_data(ORDERS_FILE)
    voorraad = load_data(VOORRAAD_FILE)

    # Omzet berekenen
    omzet = 0
    for order in orders:
        omzet += len(order["producten"]) * 100 * (1 - order.get("korting", 0)/100) * 1.21

    # Voorraadwaarde berekenen
    voorraadwaarde = 0
    for product in voorraad:
        voorraadwaarde += product.get("aantal", 0) * product.get("verkoopprijs", 0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Totaal Omzet (incl. BTW)", value=f"€ {omzet:,.2f}")
    with col2:
        st.metric(label="Totale Voorraadwaarde", value=f"€ {voorraadwaarde:,.2f}")

    # Visualisaties
    omzet_df = pd.DataFrame({
        "Categorie": ["Omzet"],
        "Bedrag": [omzet]
    })
    voorraad_df = pd.DataFrame(voorraad)

    st.subheader("📈 Omzet Grafiek")
    fig1 = px.bar(omzet_df, x="Categorie", y="Bedrag", text_auto='.2s', title="Totaal Omzet")
    st.plotly_chart(fig1)

    if not voorraad_df.empty:
        st.subheader("📊 Voorraad Verdeling")
        fig2 = px.pie(voorraad_df, names="categorie", values="aantal", title="Voorraad per Categorie")
        st.plotly_chart(fig2)
    else:
        st.info("Nog geen voorraadgegevens beschikbaar voor grafieken.")