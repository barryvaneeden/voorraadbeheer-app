import streamlit as st
from modules import orders

def main():
    st.title("Voorraadbeheer Pro V15 - Orders Module")
    orders.app()

if __name__ == "__main__":
    main()