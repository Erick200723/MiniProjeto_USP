# Para inicializar a aplicação, execute no terminal: "streamlit run main.py"
import streamlit as st
import json
from FrontEnd.interface import main
from backEnd import  Banco

def carregar_dados():
    if 'banco' not in st.session_state:
        st.session_state.banco = Banco('Meu banco')
        st.session_state.banco.carregar_dados('dados_banco.json')

if __name__ == "__main__":
    carregar_dados()

    main()