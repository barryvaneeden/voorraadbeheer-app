import streamlit as st
import json
import os

SETTINGS_FILE = "data/field_settings.json"
MODULES = ["crm", "voorraad", "orders", "facturatie", "planning"]

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({module: [] for module in MODULES}, f)

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def beheer_interface():
    st.title("Beheer Invulvelden")
    settings = load_settings()
    module = st.selectbox("Kies een module", MODULES)
    st.subheader(f"Instellingen voor {module.capitalize()}")

    if settings.get(module):
        st.write("**Huidige velden:**")
        for idx, field in enumerate(settings[module]):
            st.write(f"{idx + 1}. Label: `{field['label']}`, Type: `{field['type']}`")

    st.divider()
    st.subheader("Voeg nieuw veld toe")
    with st.form(key="add_field_form"):
        label = st.text_input("Label")
        field_type = st.selectbox("Type", ["text", "number", "email", "date", "textarea", "selectbox"])
        submitted = st.form_submit_button("Toevoegen")
        if submitted:
            if label:
                settings[module].append({"label": label, "type": field_type})
                save_settings(settings)
                st.success(f"Veld '{label}' toegevoegd aan {module}")
                st.experimental_rerun()
            else:
                st.error("Label mag niet leeg zijn!")

    st.divider()
    st.subheader("Verwijder veld")
    if settings.get(module):
        field_to_delete = st.selectbox("Kies veld om te verwijderen", [f"{idx + 1}. {field['label']}" for idx, field in enumerate(settings[module])])
        delete_button = st.button("Verwijderen")
        if delete_button:
            idx = int(field_to_delete.split(".")[0]) - 1
            deleted_label = settings[module][idx]['label']
            settings[module].pop(idx)
            save_settings(settings)
            st.success(f"Veld '{deleted_label}' verwijderd uit {module}")
            st.experimental_rerun()

def show():
    beheer_interface()