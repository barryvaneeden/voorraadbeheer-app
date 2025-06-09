import streamlit as st
from modules import planning

def main():
    st.title("Voorraadbeheer Pro V15 - Planning Module")
    planning.app()

if __name__ == "__main__":
    main()