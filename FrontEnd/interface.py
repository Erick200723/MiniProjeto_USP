# FrontEnd/tela.py
import streamlit as st
import random
import time
from datetime import datetime
from backEnd import Correntista, Banco, Investidor, Emprestimo, Transacao

def main():
    st.title("Sistema Bancário")

    menu = st.sidebar.selectbox(
        "Escolha uma opção",
        ["Criar Correntista", "Realizar Transação", "Solicitar Empréstimo", "Criar investidor" ,"Investir","Pagar Parcela"]
    )
    
    if "banco" not in st.session_state:
        st.session_state.banco = Banco("Meu Banco")

    if menu == "Criar Correntista":
        st.header("Criar Novo Correntista")
        id = st.number_input("ID do Correntista", min_value=1, step=1)
        nome = st.text_input("Nome do Correntista")
        valor_anuidade = st.number_input("Valor da Anuidade", min_value=0.0, step=0.01)
        saldo_conta = st.number_input("Saldo Inicial", min_value=0.0, step=0.01)

        if any(cliente.id == id for cliente in st.session_state.banco.clientes):
            st.warning("id ja exitesnte adicione outro")

        else:
            if st.button("Criar Correntista"):
                novo_correntista = Correntista(id, nome, valor_anuidade, saldo_conta)
                st.session_state.banco.adicionar_cliente(novo_correntista)
                st.session_state.banco.salvar_dados("dados_banco.json")
                st.success(f"Correntista {nome} criado com sucesso!")
                st.write(f"Saldo atual: R$ {novo_correntista.saldo_conta:.2f}")

    elif menu == "Realizar Transação":
        st.header("Realizar Transação")
        if not st.session_state.banco.clientes:
            st.warning("Nenhum correntista cadastrado.")
        else:
            pagador_id = st.number_input("Seu ID", min_value=1, step=1)
            beneficiario_id = st.number_input("ID do Beneficiário", min_value=1, step=1)
            valor = st.number_input("Valor da Transação", min_value=0.01, step=0.01)
            tipo = st.text_input("Tipo da Transação")

            if st.button("Realizar Transação"):
                pagador = next((c for c in st.session_state.banco.clientes if c.id == pagador_id), None)
                beneficiario = next((c for c in st.session_state.banco.clientes if c.id == beneficiario_id), None)

                if pagador and beneficiario:
                    pagador.transferencia(beneficiario, valor)
                    transacao = Transacao(
                        id_transacao=len(st.session_state.banco._transacoes) + 1, 
                        valor=valor,
                        tipo=tipo,
                        pagador_id=pagador_id,
                        beneficiario_id=beneficiario_id,
                        data=datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    )
                    st.session_state.banco.adicionar_transacao(transacao)
                    st.session_state.banco.salvar_dados("dados_banco.json")
                    st.success(f"Transação de R$ {valor:.2f} realizada com sucesso!")
                else:
                    st.error("IDs inválidos. Verifique os IDs do pagador e do beneficiário.")

    elif menu == "Solicitar Empréstimo":
        st.header("Solicitar Empréstimo")
        if not st.session_state.banco.clientes:
            st.warning("Nenhum correntista cadastrado.")
        else:
            # Captura o ID do correntista que está solicitando o empréstimo
            pagador_id = st.number_input("ID do Correntista", min_value=1, step=1)
            pagador = next((c for c in st.session_state.banco.clientes if c.id == pagador_id), None)

            if pagador is None:
                st.error("Correntista não encontrado.")
            else:
                _id_emprestimo = st.number_input("ID do Empréstimo", min_value=1, step=1)
                _valor_emprestimo = st.number_input("Valor do Empréstimo", min_value=0.01, step=0.01)
                _numero_parcelas = st.number_input("Número de Parcelas", min_value=1, step=1)

                if st.button("Solicitar Empréstimo"):
                    # Cria uma instância do Empréstimo
                    novo_emprestimo = Emprestimo(
                        id_emprestimo=_id_emprestimo,  # Nome correto do parâmetro
                        valor_emprestimo=_valor_emprestimo,  # Nome correto do parâmetro
                        numero_parcelas=_numero_parcelas,  # Nome correto do parâmetro
                        data_emprestimo=datetime.now().strftime("%Y-%m-%d"),  # Formato de data sem hora
                        correntista=pagador  # Nome correto do parâmetro
                    )
                    # Adiciona o empréstimo à lista de dívidas do correntista
                    pagador._divida_emprestimo.append(novo_emprestimo)
                    # Salva os dados no arquivo JSON
                    st.session_state.banco.salvar_dados("dados_banco.json")
                    # Exibe uma mensagem de sucesso
                    st.success(f"Empréstimo de R${_valor_emprestimo:.2f} solicitado com sucesso para o correntista {pagador.nome}.")
    elif menu == "Criar investidor":
        st.header("Criar investidor")
        investidor_id = st.number_input('Id do Investidor',min_value=1,step=1)
        nome = st.text_input('Nome do investidor')
        valor_anuidade = st.number_input('Valor da Anuidade', min_value=1, step=1)
        saldo_conta = st.number_input("Saldo da conta", min_value=1, step=1)

        if st.button('Criar Investidor'):
            if any(investido.id == investidor_id for investido in st.session_state.banco.investidor):
                st.warning("Investidor ja exitente troque o id")
            else:
                novo_envestidor = Investidor(
                    id=investidor_id,  
                    nome=nome,
                    valor_anuidade=valor_anuidade,
                    saldo_conta=saldo_conta
                )

                st.session_state.banco._investidor.append(novo_envestidor)
                st.session_state.banco.salvar_dados("dados_banco.json")
                st.success(f"Investidor {nome} criado com sucesso!")
                st.write(f"Saldo atual: R$ {novo_envestidor.saldo_conta:.2f}")
                
    if menu == "Investir":
        st.header("Fazer Investimento")
        
        if "banco" not in st.session_state:
            st.session_state.banco = Banco("Meu Banco")
            st.session_state.banco.carregar_dados("dados_banco.json")  
        
        if not st.session_state.banco.investidor:
            st.warning("Nenhum investidor cadastrado.")
        else:
            investidor_id = st.number_input("ID do Investidor", min_value=1, step=1)
            investidor = next((i for i in st.session_state.banco.investidor if i.id == investidor_id), None)
            
            if investidor:
                valor_investimento = st.number_input("Valor do Investimento", min_value=0.01, step=0.01)
                
                if st.button("Investir"):
                    try:
                        investidor.investimento(valor_investimento)
                        st.session_state.banco.salvar_dados("dados_banco.json") 
                        st.success(f"Investimento de R${valor_investimento:.2f} realizado com sucesso!")
                    except ValueError as e:
                        st.error(str(e))
            else:
                st.error("Investidor não encontrado.")

    if menu == "Pagar Parcela":
        st.header("Pagar Parcela")
        if not st.session_state.banco.clientes:
            st.warning("Nenhum correntista cadastrado.")
        else:
            correntista_id = st.number_input("ID do Correntista", min_value=1, step=1)
            correntista = next((c for c in st.session_state.banco.clientes if c.id == correntista_id), None)
            
            if correntista:
                if not correntista._divida_emprestimo:  
                    st.warning("Nenhum empréstimo encontrado para este correntista.")
                else:
                    emprestimo = correntista._divida_emprestimo[0]  
                    parcela_numero = st.number_input(
                        "Número da Parcela",
                        min_value=1,
                        max_value=len(emprestimo.lista_parcelas),  
                        step=1
                    )
                    
                    if st.button("Pagar Parcela"):
                        parcela = emprestimo.lista_parcelas[parcela_numero - 1]
                        if not parcela['paga']:
                            parcela['paga'] = True
                            emprestimo._valor_pago += parcela['valor']
                            emprestimo._valor_restante -= parcela['valor']
                            st.success(f"Parcela {parcela_numero} paga: R${parcela['valor']:.2f}")
                        else:
                            st.warning("Esta parcela já foi paga.")
            else:
                st.error("Correntista não encontrado.")
if __name__ == "__main__":
    main()