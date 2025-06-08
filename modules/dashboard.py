import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title('📊 Dashboard')

    omzet_data = {'Maand': ['Jan', 'Feb', 'Mrt', 'Apr'], 'Omzet': [12000, 15000, 10000, 17000]}
    df_omzet = pd.DataFrame(omzet_data)

    klanten_data = {'Maand': ['Jan', 'Feb', 'Mrt', 'Apr'], 'Nieuwe Klanten': [5, 8, 3, 7]}
    df_klanten = pd.DataFrame(klanten_data)

    st.subheader('Omzet per maand')
    fig1 = px.line(df_omzet, x='Maand', y='Omzet', markers=True)
    st.plotly_chart(fig1)

    st.subheader('Nieuwe klanten per maand')
    fig2 = px.bar(df_klanten, x='Maand', y='Nieuwe Klanten')
    st.plotly_chart(fig2)