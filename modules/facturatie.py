import streamlit as st
import json
import os
from fpdf import FPDF
from datetime import datetime

ORDERS_FILE = "data/orders_data.json"
FACTUREN_DIR = "facturen/"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def generate_factuurnummer():
    existing_files = os.listdir(FACTUREN_DIR)
    num = len(existing_files) + 1
    return f"2025-{str(num).zfill(4)}"

def create_factuur(order):
    factuurnummer = generate_factuurnummer()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Factuur: {factuurnummer}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Klant: {order['klant']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Datum: {datetime.now().strftime('%d-%m-%Y')}", ln=True, align="L")
    pdf.ln(10)

    subtotal = 0
    for product in order["producten"]:
        pdf.cell(200, 10, txt=f"Product: {product}", ln=True, align="L")
        subtotal += 100  # Simpel: elk product fictief 100 euro

    korting = order.get("korting", 0)
    total = subtotal * (1 - korting/100)
    btw = total * 0.21
    total_incl_btw = total + btw

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Subtotaal: € {subtotal:.2f}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Korting: {korting:.2f}%", ln=True, align="L")
    pdf.cell(200, 10, txt=f"BTW (21%): € {btw:.2f}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Totaal incl. BTW: € {total_incl_btw:.2f}", ln=True, align="L")

    file_path = os.path.join(FACTUREN_DIR, f"{factuurnummer}.pdf")
    pdf.output(file_path)
    return file_path

def app():
    st.subheader("🧾 Factuur aanmaken")
    orders = load_data(ORDERS_FILE)
    order_labels = [f"{i+1}: {order['klant']}" for i, order in enumerate(orders)]

    if not orders:
        st.warning("Nog geen orders beschikbaar.")
        return

    selected = st.selectbox("Selecteer order", order_labels)
    selected_index = int(selected.split(":")[0]) - 1
    selected_order = orders[selected_index]

    if st.button("Genereer Factuur"):
        file_path = create_factuur(selected_order)
        st.success(f"Factuur gegenereerd: {os.path.basename(file_path)}")
        with open(file_path, "rb") as f:
            st.download_button("Download Factuur", f, file_name=os.path.basename(file_path))