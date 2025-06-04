import streamlit as st
import pandas as pd
import os
import plotly.express as px
import datetime

# Configuratie
CSV_FILE = 'inventory.csv'
USERNAME = st.secrets["credentials"]["username"]
PASSWORD = st.secrets["credentials"]["password"]
ALERT_THRESHOLD = 5
MAX_DAYS_IN_STOCK = 180

# Dropdown opties
PRODUCTGROEPEN = ['Accessoires', 'Banken', 'Bedden', 'Bureaus', 'Kasten', 'Stoelen', 'Tafels']
STAAT_OPTIES = ['Nieuw', 'Licht gebruikt', 'Beschadigd']
VERVOLGACTIE_OPTIES = ['Doneren', 'Verkopen', 'Retour leverancier', 'Korting geven', 'Afvoeren']
HOUDBAARHEID_OPTIES = ['< 1 maand', '1 - 3 maanden', '3 - 6 maanden', '6 > maanden']
LOCATIE_OPTIES = ['Asscheman', 'Henneken', 'KZI - Boven', 'KZI - Hub', 'KZI - Magazijn', 'Westlandse']
VERANTWOORDELIJKEN = ['Angela', 'Arthur', 'Barry', 'Kimberley', 'Paul']
LEVERANCIERS = ['Leverancier A', 'Leverancier B', 'Leverancier C', 'Leverancier D']
REDEN_RETOUR_OPTIES = ['Overcompleet', 'Defect', 'Project beëindigd', 'Seizoensgebonden', 'Anders']

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
            'Aantal producten', 'Locatie opslag', 'Geschikt voor project',
            'Staat', 'Gewenste vervolgactie', 'Projectreferentie',
            'Inkoopwaarde', 'Verkoopwaarde', 'Verwachte houdbaarheid',
            'Interne verantwoordelijke', 'Datum toegevoegd', 'Dagen in voorraad'
        ])

def save_inventory(df):
    df.to_csv(CSV_FILE, index=False)

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def main():
    st.title("🔐 Inloggen Voorraadbeheer PRO")

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
        with st.container():
            productgroep = st.selectbox("Productgroep", PRODUCTGROEPEN)
            productnaam = st.text_input("Productnaam")
            leverancier = st.selectbox("Leverancier", LEVERANCIERS)
            afmetingen = st.text_input("Afmetingen (BxDxH in cm)")
            kleur = st.text_input("Kleur / afwerking")
            bijzonderheden = st.text_area("Bijzonderheden")
            reden_retorno = st.selectbox("Reden retour / voorraad", REDEN_RETOUR_OPTIES)
            aantal = st.number_input("Aantal producten", min_value=0, step=1)
            locatie = st.selectbox("Locatie opslag", LOCATIE_OPTIES)
            projectgeschikt = st.selectbox("Geschikt voor project", ['Ja', 'Nee'])
            staat = st.selectbox("Staat", STAAT_OPTIES)
            vervolgactie = st.selectbox("Gewenste vervolgactie", VERVOLGACTIE_OPTIES)
            projectreferentie = st.text_input("Projectreferentie")
            inkoopwaarde = st.number_input("Inkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            verkoopwaarde = st.number_input("Verkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            houdbaarheid = st.selectbox("Verwachte houdbaarheid", HOUDBAARHEID_OPTIES)
            verantwoordelijke = st.selectbox("Interne verantwoordelijke", VERANTWOORDELIJKEN)

            st.markdown("---")

            totaal_inkoop = aantal * inkoopwaarde
            totaal_verkoop = aantal * verkoopwaarde
            st.write(f"💶 **Totale inkoopwaarde:** €{totaal_inkoop:,.2f}")
            st.write(f"💶 **Totale verkoopwaarde:** €{totaal_verkoop:,.2f}")

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
                'Aantal producten': [aantal],
                'Locatie opslag': [locatie],
                'Geschikt voor project': [projectgeschikt],
                'Staat': [staat],
                'Gewenste vervolgactie': [vervolgactie],
                'Projectreferentie': [projectreferentie],
                'Inkoopwaarde': [inkoopwaarde],
                'Verkoopwaarde': [verkoopwaarde],
                'Verwachte houdbaarheid': [houdbaarheid],
                'Interne verantwoordelijke': [verantwoordelijke],
                'Datum toegevoegd': [pd.Timestamp.now()],
                'Dagen in voorraad': [0]
            })
            inventory = pd.concat([inventory, new_product], ignore_index=True)
            save_inventory(inventory)
            st.success(f"Product '{productnaam}' toegevoegd!")
        elif submitted:
            st.error("Productnaam is verplicht.")

    # Filters en bestaande voorraad tonen
    st.subheader("📋 Huidige Voorraad")
    st.dataframe(inventory)

    # Download knop
    st.subheader("⬇️ Download Voorraadlijst")
    csv = inventory.to_csv(index=False).encode('utf-8')
    st.download_button("Download als CSV", data=csv, file_name='voorraad.csv', mime='text/csv')

if __name__ == "__main__":
    main()