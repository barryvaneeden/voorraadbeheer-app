import streamlit as st
import json
import os

DATA_FILE = "data/crm_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def app():
    st.subheader("➕ Nieuwe klant toevoegen")
    data = load_data()

    with st.form("crm_form", clear_on_submit=True):
        naam = st.text_input("Naam")
        bedrijf = st.text_input("Bedrijf")
        email = st.text_input("E-mail")
        telefoon = st.text_input("Telefoon")
        tags = st.text_input("Tags (komma gescheiden)")
        uploaded_file = st.file_uploader("Upload bestand (PDF/JPG/PNG)", type=["pdf", "jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Toevoegen")

        if submitted:
            klant = {
                "naam": naam,
                "bedrijf": bedrijf,
                "email": email,
                "telefoon": telefoon,
                "tags": [tag.strip() for tag in tags.split(",")],
                "bestand": uploaded_file.name if uploaded_file else None,
            }
            if uploaded_file:
                upload_path = os.path.join("uploads", uploaded_file.name)
                with open(upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            data.append(klant)
            save_data(data)
            st.success(f"Klant {naam} toegevoegd!")

    st.subheader("📋 Overzicht klanten")
    if data:
        for idx, klant in enumerate(data):
            st.write(f"**{klant['naam']}** - {klant['bedrijf']} - {klant['email']}")
            st.write(f"Telefoon: {klant['telefoon']}")
            st.write(f"Tags: {', '.join(klant['tags'])}")
            if klant["bestand"]:
                st.markdown(f"[Download bestand](uploads/{klant['bestand']})")
    else:
        st.info("Nog geen klanten toegevoegd.")