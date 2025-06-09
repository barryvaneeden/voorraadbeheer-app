import streamlit as st
import json
import os
import pandas as pd

DATA_FILE = "data/crm_data.json"
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
    for key in item.keys():
        if 'naam' in key.lower() or 'bedrijf' in key.lower():
            return item[key]
    return None

def interface():
    st.title("Crm")

    settings = load_settings()
    fields = settings.get("crm", [])
    crm_data = load_crm_data()

    st.subheader("Nieuw Item Toevoegen")
    with st.form(key="crm_form"):
        new_record = {}

        if "crm" == "orders":
            klanten = [get_best_crm_field(item) for item in crm_data if get_best_crm_field(item)]
            if klanten:
                new_record["Klant"] = st.selectbox("Selecteer Klant", klanten)
            else:
                st.warning("Geen geschikte klanten gevonden in CRM.")
        elif "crm" == "voorraad":
            leveranciers = [get_best_crm_field(item) for item in crm_data if get_best_crm_field(item)]
            if leveranciers:
                new_record["Leverancier"] = st.selectbox("Selecteer Leverancier", leveranciers)
            else:
                st.warning("Geen geschikte leveranciers gevonden in CRM.")

        for field in fields:
            label = field["label"]
            field_type = field["type"]
            default = field.get("default", "")

            if field_type == "text":
                new_record[label] = st.text_input(label, value=default)
            elif field_type == "number":
                new_record[label] = st.number_input(label, value=float(default) if default else 0)
            elif field_type == "email":
                new_record[label] = st.text_input(label, value=default, placeholder="jouw@email.nl")
            elif field_type == "date":
                new_record[label] = st.date_input(label)
            elif field_type == "textarea":
                new_record[label] = st.text_area(label, value=default)
            elif field_type == "selectbox":
                options = st.text_input(f"Opties voor {label} (komma gescheiden)")
                if options:
                    options_list = [opt.strip() for opt in options.split(",")]
                    new_record[label] = st.selectbox(label, options_list)
                else:
                    new_record[label] = ""
            elif field_type == "status":
                new_record[label] = st.selectbox(label, ["Open", "Afgerond", "Geannuleerd"])

        submitted = st.form_submit_button("Opslaan")

        if submitted:
            for field in fields:
                if field.get("required") and not new_record.get(field["label"]):
                    st.error(f"Veld '{field['label']}' is verplicht!")
                    return
            data = load_data()
            data.append(new_record)
            save_data(data)
            st.success("Nieuw item toegevoegd!")
            st.rerun()

    st.subheader("Bestaande Items")
    data = load_data()
    if data:
        df = pd.DataFrame(data)
        search = st.text_input("Zoeken in gegevens...")
        if search:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        st.dataframe(df)
        st.download_button("Download data als CSV", df.to_csv(index=False).encode("utf-8"), "data.csv", "text/csv")
    else:
        st.info("Nog geen items toegevoegd.")

def show():
    interface()