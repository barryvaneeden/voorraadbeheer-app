import streamlit as st
from modules import facturatie

def main():
    st.title("Voorraadbeheer Pro V15 - Facturatie Module")
    facturatie.app()

if __name__ == "__main__":
    main()