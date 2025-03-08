import streamlit as st
from backEnd.logica import minha_logica

def main():
    st.title("Gerenciador de Tarefas!")

    if "tarefas" not in st.session_state:
        st.session_state.tarefas = minha_logica()

    #campo para adicionar as tarefas

    nova_tarefa = st.text_input("Digite a tarefa que deseja fazer!")
    if st.button("Adicionar"):
        st.session_state.tarefas.adcionar_tarefa(nova_tarefa)
        st.write("Tarefa adicionada com sucesso!")
        st.experimental_rerun()

