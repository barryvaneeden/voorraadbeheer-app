import streamlit as st
import json
import os

DATA_FILE = "data/voorraad_data.json"
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

def get_best_crm_field(item):
    # Zoek dynamisch naar veld met 'naam' of 'bedrijf'
    for key in item.keys():
        if 'naam' in key.lower() or 'bedrijf' in key.lower():
            return item[key]
    return None

def interface():
    st.title("Voorraad")

    settings = load_settings()
    fields = settings.get("voorraad", [])
    crm_data = load_crm_data()

    st.subheader("Nieuw Item Toevoegen")
    with st.form(key="voorraad_form"):
        new_record = {}

        # Speciaal: CRM koppeling
        if "voorraad" == "orders":
            klanten = [get_best_crm_field(item) for item in crm_data if get_best_crm_field(item)]
            if klanten:
                new_record["Klant"] = st.selectbox("Selecteer Klant", klanten)
            else:
                st.warning("Geen geschikte klanten gevonden in CRM.")
        elif "voorraad" == "voorraad":
            leveranciers = [get_best_crm_field(item) for item in crm_data if get_best_crm_field(item)]
            if leveranciers:
                new_record["Leverancier"] = st.selectbox("Selecteer Leverancier", leveranciers)
            else:
                st.warning("Geen geschikte leveranciers gevonden in CRM.")

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