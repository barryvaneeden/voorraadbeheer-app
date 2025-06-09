import streamlit as st
import json
import os

DATA_FILE = "data/orders_data.json"
SETTINGS_FILE = "data/field_settings.json"
CRM_FILE = "data/crm_data.json"

def load_crm_data():
    if os.path.exists(CRM_FILE):
        with open(CRM_FILE, "r") as f:
            return json.load(f)
    return []

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def interface():
    st.title("Orders")

    settings = load_settings()
    fields = settings.get("orders", [])
    crm_data = load_crm_data()

    st.subheader("Nieuw Item Toevoegen")
    with st.form(key="orders_form"):
        new_record = {}

        # Speciaal: CRM koppeling
        if "orders" == "orders":
            klanten = [item.get("Bedrijfsnaam", "Onbekend") for item in crm_data]
            new_record["Klant"] = st.selectbox("Selecteer Klant", klanten)
        elif "orders" == "voorraad":
            leveranciers = [item.get("Bedrijfsnaam", "Onbekend") for item in crm_data]
            new_record["Leverancier"] = st.selectbox("Selecteer Leverancier", leveranciers)

        for field in fields:
            label = field["label"]
            field_type = field["type"]

            if field_type == "text":
                new_record[label] = st.text_input(label)
            elif field_type == "number":
                new_record[label] = st.number_input(label, step=1)
            elif field_type == "email":
                new_record[label] = st.text_input(label, placeholder="jouw@email.nl")
            elif field_type == "date":
                new_record[label] = st.date_input(label).isoformat()
            elif field_type == "textarea":
                new_record[label] = st.text_area(label)
            elif field_type == "selectbox":
                options = st.text_input(f"Opties voor {label} (komma gescheiden)")
                if options:
                    options_list = [opt.strip() for opt in options.split(",")]
                    new_record[label] = st.selectbox(label, options_list)
                else:
                    new_record[label] = ""

        submitted = st.form_submit_button("Opslaan")

        if submitted:
            # Controleren op lege velden
            if any(value == "" or value is None for value in new_record.values()):
                st.error("Vul alle velden in!")
            else:
                data = load_data()
                data.append(new_record)
                save_data(data)
                st.success("Nieuw item toegevoegd!")
                st.rerun()

    st.subheader("Bestaande Items")
    data = load_data()
    if data:
        st.dataframe(data)
    else:
        st.info("Nog geen items toegevoegd.")

def show():
    interface()