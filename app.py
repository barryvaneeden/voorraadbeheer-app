import streamlit as st
import pandas as pd
import os
import plotly.express as px
import datetime

# Configuratie
CSV_FILE = 'inventory.csv'
USERNAME = 'admin'
PASSWORD = 'voorraad123'
ALERT_THRESHOLD = 5  # Waarschuw als aantal lager is dan dit getal

# Functies
def load_inventory():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Naam', 'Aantal', 'Waarde', 'Categorie', 'Datum'])

def save_inventory(df):
    df.to_csv(CSV_FILE, index=False)

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def main():
    st.title("🔐 Inloggen Voorraadbeheer")

    # Inlog
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    if st.button("Inloggen"):
        if authenticate(username, password):
            st.success("Inloggen gelukt!")
            voorraadbeheer()
        else:
            st.error("Ongeldige inloggegevens.")

def voorraadbeheer():
    st.title("📦 Voorraadbeheer")

    inventory = load_inventory()

    # Nieuw product toevoegen
    st.subheader("➕ Nieuw product toevoegen")
    with st.form("add_product"):
        name = st.text_input("Productnaam")
        quantity = st.number_input("Aantal", min_value=0, step=1)
        value = st.number_input("Waarde per stuk (€)", min_value=0.0, format="%.2f")
        category = st.text_input("Categorie")
        submitted = st.form_submit_button("Toevoegen")

        if submitted:
            new_product = pd.DataFrame({
                'Naam': [name],
                'Aantal': [quantity],
                'Waarde': [value],
                'Categorie': [category],
                'Datum': [datetime.datetime.now().strftime('%Y-%m-%d')]
            })
            inventory = pd.concat([inventory, new_product], ignore_index=True)
            save_inventory(inventory)
            st.success(f"Product '{name}' toegevoegd!")

    # Filters
    st.subheader("🔍 Filter op categorie")
    categories = inventory['Categorie'].dropna().unique().tolist()
    selected_category = st.selectbox("Selecteer categorie", ["Alles"] + categories)

    if selected_category != "Alles":
        filtered_inventory = inventory[inventory['Categorie'] == selected_category]
    else:
        filtered_inventory = inventory

    st.subheader("📋 Huidige Voorraad")
    st.dataframe(filtered_inventory)

    # Alerts
    st.subheader("⚠️ Waarschuwingen lage voorraad")
    low_stock = inventory[inventory['Aantal'] <= ALERT_THRESHOLD]
    if not low_stock.empty:
        st.warning("Let op! Sommige producten hebben lage voorraad:")
        st.dataframe(low_stock[['Naam', 'Aantal']])

    # Product verwijderen
    st.subheader("🗑️ Product verwijderen")
    product_to_delete = st.selectbox("Selecteer een product om te verwijderen", inventory['Naam'].tolist())
    if st.button("Verwijder product"):
        inventory = inventory[inventory['Naam'] != product_to_delete]
        save_inventory(inventory)
        st.success(f"Product '{product_to_delete}' verwijderd!")

    # Totale waarde
    st.subheader(f"💰 Totale voorraadwaarde: €{(inventory['Aantal'] * inventory['Waarde']).sum():.2f}")

    # Grafiek voorraadwaarde over tijd
    st.subheader("📈 Voorraadwaarde over tijd")
    if not inventory.empty:
        inventory['Datum'] = pd.to_datetime(inventory['Datum'])
        inventory_grouped = inventory.groupby('Datum').apply(lambda x: (x['Aantal'] * x['Waarde']).sum()).reset_index()
        inventory_grouped.columns = ['Datum', 'Totale waarde']
        fig = px.line(inventory_grouped, x='Datum', y='Totale waarde', title='Voorraadwaarde over tijd')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()