import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

DATA_FILE = "data/planning_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def app():
    st.subheader("➕ Nieuw project toevoegen")
    data = load_data()

    with st.form("planning_form", clear_on_submit=True):
        projectnaam = st.text_input("Projectnaam")
        startdatum = st.date_input("Startdatum")
        einddatum = st.date_input("Einddatum")
        status = st.selectbox("Status", ["In Planning", "Actief", "Afgerond"])

        submitted = st.form_submit_button("Toevoegen")

        if submitted:
            project = {
                "projectnaam": projectnaam,
                "startdatum": str(startdatum),
                "einddatum": str(einddatum),
                "status": status
            }
            data.append(project)
            save_data(data)
            st.success(f"Project {projectnaam} toegevoegd!")

    st.subheader("📋 Overzicht projecten")
    if data:
        df = pd.DataFrame(data)
        fig = px.timeline(
            df,
            x_start="startdatum",
            x_end="einddatum",
            y="projectnaam",
            color="status",
            title="Project Planning Gantt Chart"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nog geen projecten toegevoegd.")