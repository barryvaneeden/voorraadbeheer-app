import streamlit as st
from modules import dashboard

def main():
    st.title("Voorraadbeheer Pro V15 - Dashboard Module")
    dashboard.app()

if __name__ == "__main__":
    main()