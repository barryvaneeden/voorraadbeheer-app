import streamlit as st
import modules.crm as crm
import modules.voorraad as voorraad
import modules.orders as orders
import modules.facturatie as facturatie
import modules.planning as planning
import modules.dashboard as dashboard
import modules.beheer as beheer

st.sidebar.title("Navigatie")
menu = st.sidebar.selectbox("Selecteer een module", ["Dashboard", "CRM", "Voorraad", "Orders", "Facturatie", "Planning", "Beheer"])

if menu == "CRM":
    crm.show()
elif menu == "Voorraad":
    voorraad.show()
elif menu == "Orders":
    orders.show()
elif menu == "Facturatie":
    facturatie.show()
elif menu == "Planning":
    planning.show()
elif menu == "Dashboard":
    dashboard.show()
elif menu == "Beheer":
    beheer.show()