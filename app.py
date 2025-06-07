import streamlit as st
import pandas as pd
import os
import plotly.express as px
import datetime
import json

# Configuratie
CSV_FILE = 'inventory.csv'
SETTINGS_FILE = 'instellingen.json'
USERNAME = st.secrets["credentials"]["username"]
PASSWORD = st.secrets["credentials"]["password"]
ALERT_THRESHOLD = 5
MAX_DAYS_IN_STOCK = 180

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

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    else:
        settings = {
            "Productgroepen": [],
            "Leveranciers": [],
            "RedenRetour": [],
            "Staten": [],
            "Vervolgacties": [],
            "Verantwoordelijken": []
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
        return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def main():
    st.title("🔐 Inloggen Voorraadbeheer PRO")

    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    if st.button("Inloggen"):
        if authenticate(username, password):
            st.success("Inloggen gelukt!")
            tabs()
        else:
            st.error("Ongeldige inloggegevens.")

def tabs():
    tab1, tab2 = st.tabs(["📦 Voorraadbeheer", "⚙️ Beheer Instellingen"])
    with tab1:
        voorraadbeheer()
    with tab2:
        beheer_instellingen()

def voorraadbeheer():
    st.header("📦 Voorraadbeheer")
    settings = load_settings()
    inventory = load_inventory()

    st.subheader("➕ Nieuw product toevoegen")
    with st.form("add_product"):
        with st.container():
            productgroep = st.selectbox("Productgroep", settings['Productgroepen'])
            productnaam = st.text_input("Productnaam")
            leverancier = st.selectbox("Leverancier", settings['Leveranciers'])
            afmetingen = st.text_input("Afmetingen (BxDxH in cm)")
            kleur = st.text_input("Kleur / afwerking")
            bijzonderheden = st.text_area("Bijzonderheden")
            reden_retorno = st.selectbox("Reden retour / voorraad", settings['RedenRetour'])
            aantal = st.number_input("Aantal producten", min_value=0, step=1)
            locatie = st.text_input("Locatie opslag")
            projectgeschikt = st.selectbox("Geschikt voor project", ['Ja', 'Nee'])
            staat = st.selectbox("Staat", settings['Staten'])
            vervolgactie = st.selectbox("Gewenste vervolgactie", settings['Vervolgacties'])
            projectreferentie = st.text_input("Projectreferentie")
            inkoopwaarde = st.number_input("Inkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            verkoopwaarde = st.number_input("Verkoopwaarde (€)", min_value=0.0, step=0.01, format="%.2f")
            houdbaarheid = st.text_input("Verwachte houdbaarheid")
            verantwoordelijke = st.selectbox("Interne verantwoordelijke", settings['Verantwoordelijken'])

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

    st.subheader("📋 Huidige Voorraad")
    st.dataframe(inventory)

    st.subheader("⬇️ Download Voorraadlijst")
    csv = inventory.to_csv(index=False).encode('utf-8')
    st.download_button("Download als CSV", data=csv, file_name='voorraad.csv', mime='text/csv')

def beheer_instellingen():
    st.header("⚙️ Beheer Instellingen")
    settings = load_settings()

    optie = st.selectbox("Welke instellingen wil je beheren?", list(settings.keys()))

    st.subheader(f"Huidige {optie}:")
    st.write(settings[optie])

    with st.form(f"beheer_{optie}"):
        nieuwe_waarde = st.text_input(f"Nieuwe waarde toevoegen aan {optie}")
        te_wijzigen = st.selectbox(f"Kies bestaande waarde om te wijzigen", [""] + settings[optie])
        nieuwe_naam = st.text_input(f"Nieuwe naam voor wijziging")
        te_verwijderen = st.selectbox(f"Kies bestaande waarde om te verwijderen", [""] + settings[optie])
        submitted = st.form_submit_button("Opslaan wijzigingen")

        if submitted:
            changed = False
            if nieuwe_waarde and nieuwe_waarde not in settings[optie]:
                settings[optie].append(nieuwe_waarde)
                st.success(f"Toegevoegd: {nieuwe_waarde}")
                changed = True

            if te_wijzigen and nieuwe_naam:
                index = settings[optie].index(te_wijzigen)
                settings[optie][index] = nieuwe_naam
                st.success(f"Gewijzigd: {te_wijzigen} naar {nieuwe_naam}")
                changed = True

            if te_verwijderen:
                settings[optie].remove(te_verwijderen)
                st.success(f"Verwijderd: {te_verwijderen}")
                changed = True

            if changed:
                save_settings(settings)

if __name__ == "__main__":
    main()