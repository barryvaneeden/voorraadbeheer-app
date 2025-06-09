import streamlit as st
from modules import crm

def main():
    st.title("Voorraadbeheer Pro V15 - CRM Module")
    crm.app()

if __name__ == "__main__":
    main()