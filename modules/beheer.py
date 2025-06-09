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
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{idx + 1}. Label: `{field['label']}`, Type: `{field['type']}`" +
                         (", Required" if field.get("required") else "") +
                         (f", Default: {field.get('default', '')}" if field.get("default") else ""))
            with col2:
                if st.button("🔼", key=f"up_{idx}") and idx > 0:
                    settings[module][idx], settings[module][idx - 1] = settings[module][idx - 1], settings[module][idx]
                    save_settings(settings)
                    st.rerun()
            with col3:
                if st.button("🔽", key=f"down_{idx}") and idx < len(settings[module]) - 1:
                    settings[module][idx], settings[module][idx + 1] = settings[module][idx + 1], settings[module][idx]
                    save_settings(settings)
                    st.rerun()
            with col4:
                if st.button("❌", key=f"del_{idx}"):
                    settings[module].pop(idx)
                    save_settings(settings)
                    st.rerun()

    st.divider()
    st.subheader("Voeg nieuw veld toe")
    with st.form(key="add_field_form"):
        label = st.text_input("Label")
        field_type = st.selectbox("Type", ["text", "number", "email", "date", "textarea", "selectbox", "status"])
        required = st.checkbox("Verplicht veld?")
        default = st.text_input("Standaardwaarde (optioneel)")
        submitted = st.form_submit_button("Toevoegen")
        if submitted:
            if label:
                new_field = {"label": label, "type": field_type}
                if required:
                    new_field["required"] = True
                if default:
                    new_field["default"] = default
                settings[module].append(new_field)
                save_settings(settings)
                st.success(f"Veld '{label}' toegevoegd aan {module}")
                st.rerun()
            else:
                st.error("Label mag niet leeg zijn!")

def show():
    beheer_interface()