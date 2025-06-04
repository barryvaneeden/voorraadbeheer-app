import streamlit as st
import pandas as pd
import os
import plotly.express as px
import datetime

# Configuratie
CSV_FILE = 'inventory.csv'
USERNAME = st.secrets["credentials"]["username"]
PASSWORD = st.secrets["credentials"]["password"]
ALERT_THRESHOLD = 5  # Waarschuw als aantal lager is dan dit getal
MAX_DAYS_IN_STOCK = 180  # Waarschuw als langer dan 180 dagen in voorraad

# Dropdown opties
PRODUCTGROEPEN = ['Accessoires', 'Banken', 'Bedden', 'Bureau\'s', 'Kasten', 'Stoelen', 'Tafels']
STAAT_OPTIES = ['Nieuw', 'Licht gebruikt', 'Beschadigd']
INZETBAARHEID_OPTIES = ['Ja', 'Nee']
VERVOLGACTIE_OPTIES = ['Doneren', 'Verkopen', 'Retour leverancier', 'Korting geven', 'Afvoeren']
HOUDBAARHEID_OPTIES = ['< 1 maand', '1 - 3 maanden', '3 - 6 maanden', '6 > maanden']
GEOOGDE_PROJECTEN = ['Entree', 'Kantoor', 'Lounge', 'Zorg']
LOCATIE_OPTIES = ['Asscheman', 'Henneken', 'KZI - Boven', 'KZI - Hub', 'KZI - Magazijn', 'Westlandse']
VERANTWOORDELIJKEN = ['Angela', 'Arthur', 'Barry', 'Kimberley', 'Paul']

# Functies
def load_inventory():
    if os.path.exists(CSV_FILE):
        inventory = pd.read_csv(CSV_FILE)
        inventory['Datum toegevoegd'] = pd.to_datetime(inventory['Datum toegevoegd'])
        inventory['Dagen in voorraad'] = (pd.Timestamp.now() - inventory['Datum toegevoegd']).dt.days
        return inventory
    else:
        return pd.DataFrame(columns=[
            'Productgroep', 'Productnaam', 'Leverancier', 'Afmetingen',
            'Kleur / afwerking', 'Bijzonderheden', 'Reden retour / voorraad',
            'Aantal op voorraad', 'Locatie opslag', 'Geschikt voor project',
            'Staat', 'Gewenste vervolgactie', 'Projectreferentie',
            'Inkoopwaarde', 'Verkoopwaarde', 'Verwachte houdbaarheid',
            'Interne verantwoordelijke', 'Inzetbaarheid',
            'Datum toegevoegd', 'Dagen in voorraad'
        ])

def save_inventory(df):
    df.to_csv(CSV_FILE, index=False)

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def main():
    st.title("🔐 Inloggen Voorraadbeheer PRO")

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
    st.title("📦 Voorraadbeheer PRO")

    inventory = load_inventory()

    # Nieuw product toevoegen
    st.subheader("➕ Nieuw product toevoegen")
    with st.form("add_product"):
        col1, col2 = st.columns(2)
        with col1:
            productgroep = st.selectbox("Productgroep", PRODUCTGROEPEN)
            productnaam = st.text_input("Productnaam")
            leverancier = st.text_input("Leverancier")
            afmetingen = st.text_input("Afmetingen (BxDxH in cm)")
            kleur = st.text_input("Kleur / afwerking")
            bijzonderheden = st.text_area("Bijzonderheden")
            reden_retorno = st.text_input("Reden retour / voorraad")
            aantal = st.number_input("Aantal op voorraad", min_value=0, step=1)
        with col2:
            locatie = st.selectbox("Locatie opslag", LOCATIE_OPTIES)
            projectgeschikt = st.selectbox("Geschikt voor project", ['Ja', 'Nee'])
            staat = st.selectbox("Staat", STAAT_OPTIES)
            vervolgactie = st.selectbox("Gewenste vervolgactie", VERVOLGACTIE_OPTIES)
            projectreferentie = st.text_input("Projectreferentie")
            inkoopwaarde = st.number_input("Inkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            verkoopwaarde = st.number_input("Verkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            houdbaarheid = st.selectbox("Verwachte houdbaarheid", HOUDBAARHEID_OPTIES)
            verantwoordelijke = st.selectbox("Interne verantwoordelijke", VERANTWOORDELIJKEN)
            inzetbaarheid = st.selectbox("Inzetbaarheid", INZETBAARHEID_OPTIES)

        submitted = st.form_submit_button("Toevoegen")
        if submitted and productnaam:
            new_product = pd.DataFrame({
                'Productgroep': [productgroep],
                'Productnaam': [productnaam],
                'Leverancier': [leverancier],
                'Afmetingen': [afmetingen],
                'Kleur / afwerking': [kleur],
                'Bijzonderheden': [bijzonderheden],
                'Reden retour / voorraad': [reden_retorno],
                'Aantal op voorraad': [aantal],
                'Locatie opslag': [locatie],
                'Geschikt voor project': [projectgeschikt],
                'Staat': [staat],
                'Gewenste vervolgactie': [vervolgactie],
                'Projectreferentie': [projectreferentie],
                'Inkoopwaarde': [inkoopwaarde],
                'Verkoopwaarde': [verkoopwaarde],
                'Verwachte houdbaarheid': [houdbaarheid],
                'Interne verantwoordelijke': [verantwoordelijke],
                'Inzetbaarheid': [inzetbaarheid],
                'Datum toegevoegd': [pd.Timestamp.now()],
                'Dagen in voorraad': [0]
            })
            inventory = pd.concat([inventory, new_product], ignore_index=True)
            save_inventory(inventory)
            st.success(f"Product '{productnaam}' toegevoegd!")
        elif submitted:
            st.error("Productnaam is verplicht.")

    # Filters
    st.subheader("🔍 Filteren")
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_productgroep = st.selectbox("Filter op productgroep", ["Alles"] + PRODUCTGROEPEN)
        selected_staat = st.selectbox("Filter op staat", ["Alles"] + STAAT_OPTIES)
    with filter_col2:
        selected_verantwoordelijke = st.selectbox("Filter op verantwoordelijke", ["Alles"] + VERANTWOORDELIJKEN)
        selected_inzetbaarheid = st.selectbox("Filter op inzetbaarheid", ["Alles"] + INZETBAARHEID_OPTIES)

    filtered_inventory = inventory.copy()
    if selected_productgroep != "Alles":
        filtered_inventory = filtered_inventory[filtered_inventory['Productgroep'] == selected_productgroep]
    if selected_staat != "Alles":
        filtered_inventory = filtered_inventory[filtered_inventory['Staat'] == selected_staat]
    if selected_verantwoordelijke != "Alles":
        filtered_inventory = filtered_inventory[filtered_inventory['Interne verantwoordelijke'] == selected_verantwoordelijke]
    if selected_inzetbaarheid != "Alles":
        filtered_inventory = filtered_inventory[filtered_inventory['Inzetbaarheid'] == selected_inzetbaarheid]

    st.subheader("📋 Huidige Voorraad")
    st.dataframe(filtered_inventory)

    # Alerts
    st.subheader("⚠️ Alerts")
    low_stock = inventory[inventory['Aantal op voorraad'] <= ALERT_THRESHOLD]
    long_stock = inventory[inventory['Dagen in voorraad'] > MAX_DAYS_IN_STOCK]
    not_inzetbaar = inventory[inventory['Inzetbaarheid'] == 'Nee']

    if not low_stock.empty:
        st.warning("Let op! Sommige producten hebben lage voorraad:")
        st.dataframe(low_stock[['Productnaam', 'Aantal op voorraad']])

    if not long_stock.empty:
        st.warning("Let op! Sommige producten liggen te lang op voorraad:")
        st.dataframe(long_stock[['Productnaam', 'Dagen in voorraad']])

    if not not_inzetbaar.empty:
        st.warning("Let op! Sommige producten zijn niet inzetbaar:")
        st.dataframe(not_inzetbaar[['Productnaam', 'Inzetbaarheid']])

    # Grafieken
    st.subheader("📊 Overzicht Grafieken")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(inventory, names='Productgroep', title='Verdeling Productgroepen')
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.pie(inventory, names='Staat', title='Verdeling Staat Producten')
        st.plotly_chart(fig2)

    fig3 = px.pie(inventory, names='Inzetbaarheid', title='Inzetbaarheid Verdeling')
    st.plotly_chart(fig3)

    # Download knop
    st.subheader("⬇️ Download Voorraadlijst")
    csv = inventory.to_csv(index=False).encode('utf-8')
    st.download_button("Download als CSV", data=csv, file_name='voorraad.csv', mime='text/csv')

if __name__ == "__main__":
    main()