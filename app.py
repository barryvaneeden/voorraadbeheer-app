import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
import datetime

# Config
CSV_FILE = 'inventory.csv'
SETTINGS_FILE = 'instellingen.json'
USERNAME = st.secrets["credentials"]["username"]
PASSWORD = st.secrets["credentials"]["password"]

# Load & Save Functions
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
            "Productgroepen": [], "Leveranciers": [], "RedenRetour": [],
            "LocatieOpslag": [], "GeschiktProject": [], "Staten": [],
            "Vervolgacties": [], "Projectreferenties": [], "Houdbaarheid": [],
            "Verantwoordelijken": []
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
        return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Auth
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

def login():
    st.title("🔐 Inloggen Voorraadbeheer PRO")
    username = st.text_input("Gebruikersnaam")
    password = st.text_input("Wachtwoord", type="password")
    if st.button("Inloggen"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.success("Inloggen gelukt!")
        else:
            st.error("Ongeldige inloggegevens.")

# Dashboard
def show_dashboard(inventory):
    st.title("📊 Dashboard")
    total_products = inventory['Aantal producten'].sum()
    total_sales = (inventory['Aantal producten'] * inventory['Verkoopwaarde']).sum()
    avg_days = inventory['Dagen in voorraad'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Aantal producten", f"{total_products}")
    col2.metric("💶 Totale verkoopwaarde (€)", f"{total_sales:,.2f}")
    col3.metric("📅 Gemiddelde voorraadduur", f"{avg_days:.1f} dagen")

    st.markdown("---")

    st.subheader("📈 Voorraadwaarde per productgroep")
    if not inventory.empty:
        group_data = inventory.groupby('Productgroep').agg({'Aantal producten':'sum', 'Verkoopwaarde':'mean'}).reset_index()
        fig = px.bar(group_data, x='Productgroep', y='Aantal producten', color='Productgroep', title="Aantal producten per productgroep")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("📋 Laatste 5 Toegevoegde Producten")
    st.dataframe(inventory.sort_values(by='Datum toegevoegd', ascending=False).head(5))

# Voorraad
def show_inventory(inventory):
    st.title("📦 Voorraadlijst")
    with st.expander("🔎 Filters"):
        productgroep_filter = st.selectbox("Filter op productgroep", ["Alle"] + list(inventory['Productgroep'].unique()))
        if productgroep_filter != "Alle":
            inventory = inventory[inventory['Productgroep'] == productgroep_filter]
    st.dataframe(inventory)

# Product Toevoegen
def show_add_product(settings):
    st.title("➕ Nieuw product toevoegen")
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
            locatie = st.selectbox("Locatie opslag", settings['LocatieOpslag'])
            projectgeschikt = st.selectbox("Geschikt voor project", settings['GeschiktProject'])
            staat = st.selectbox("Staat", settings['Staten'])
            vervolgactie = st.selectbox("Gewenste vervolgactie", settings['Vervolgacties'])
            projectreferentie = st.selectbox("Projectreferentie", settings['Projectreferenties'])
            inkoopwaarde = st.number_input("Inkoopwaarde (€)", min_value=0.0, step=0.01)
            verkoopwaarde = st.number_input("Verkoopwaarde (€)", min_value=0.0, step=0.01)
            houdbaarheid = st.selectbox("Verwachte houdbaarheid", settings['Houdbaarheid'])
            verantwoordelijke = st.selectbox("Interne verantwoordelijke", settings['Verantwoordelijken'])

            totaal_inkoop = aantal * inkoopwaarde
            totaal_verkoop = aantal * verkoopwaarde
            st.write(f"💶 **Totale inkoopwaarde:** €{totaal_inkoop:,.2f}")
            st.write(f"💶 **Totale verkoopwaarde:** €{totaal_verkoop:,.2f}")

        submitted = st.form_submit_button("Toevoegen")
        if submitted and productnaam:
            inventory = load_inventory()
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

# Instellingen beheren
def show_settings(settings):
    st.title("⚙️ Beheer Instellingen")
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

# App Flow
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        st.sidebar.title("🛠️ RENDER")
        page = st.sidebar.radio("Navigatie", ["🏠 Dashboard", "📦 Voorraadlijst", "➕ Nieuw product", "⚙️ Instellingen", "🚪 Uitloggen"])
        settings = load_settings()
        inventory = load_inventory()

        if page == "🏠 Dashboard":
            show_dashboard(inventory)
        elif page == "📦 Voorraadlijst":
            show_inventory(inventory)
        elif page == "➕ Nieuw product":
            show_add_product(settings)
        elif page == "⚙️ Instellingen":
            show_settings(settings)
        elif page == "🚪 Uitloggen":
            st.session_state['logged_in'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()