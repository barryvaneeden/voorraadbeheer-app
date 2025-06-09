import streamlit as st
import json
import os

DATA_FILE = "data/voorraad_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def app():
    st.subheader("➕ Nieuw product toevoegen")
    data = load_data()

    with st.form("voorraad_form", clear_on_submit=True):
        naam = st.text_input("Productnaam")
        artikelnummer = st.text_input("Artikelnummer")
        categorie = st.selectbox("Categorie", ["Stoelen", "Tafels", "Bureaus"])
        inkoopprijs = st.number_input("Inkoopprijs", min_value=0.0, step=0.01)
        verkoopprijs = st.number_input("Verkoopprijs", min_value=0.0, step=0.01)
        aantal = st.number_input("Aantal op voorraad", min_value=0, step=1)
        uploaded_file = st.file_uploader("Upload productfoto (JPG/PNG)", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Toevoegen")

        if submitted:
            product = {
                "naam": naam,
                "artikelnummer": artikelnummer,
                "categorie": categorie,
                "inkoopprijs": inkoopprijs,
                "verkoopprijs": verkoopprijs,
                "aantal": aantal,
                "foto": uploaded_file.name if uploaded_file else None,
            }
            if uploaded_file:
                upload_path = os.path.join("uploads", uploaded_file.name)
                with open(upload_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            data.append(product)
            save_data(data)
            st.success(f"Product {naam} toegevoegd!")

    st.subheader("📋 Overzicht voorraad")
    if data:
        for idx, product in enumerate(data):
            st.write(f"**{product['naam']}** - {product['artikelnummer']} - {product['categorie']}")
            st.write(f"Inkoopprijs: €{product['inkoopprijs']} | Verkoopprijs: €{product['verkoopprijs']} | Aantal: {product['aantal']}")
            if product["foto"]:
                st.image(f"uploads/{product['foto']}", width=150)
    else:
        st.info("Nog geen producten toegevoegd.")