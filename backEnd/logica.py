import datetime
import json
from typing import List
from datetime import datetime

class Correntista:
    def __init__(self, id: int, nome: str, valor_anuidade: float, saldo_conta: float):
        self._id = id
        self._nome = nome
        self._valor_anuidade = valor_anuidade
        self._saldo_conta = saldo_conta
        self._lista_credito = []
        self._extrato_banco = []
        self._divida_emprestimo = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def valor_anuidade(self) -> float:
        return self._valor_anuidade

    @property
    def saldo_conta(self) -> float:
        return self._saldo_conta

    @saldo_conta.setter
    def saldo_conta(self, valor: float):
        if valor < 0:
            raise ValueError("O saldo da conta não pode ser negativo.")
        self._saldo_conta = valor

    @property
    def lista_credito(self) -> list:
        return self._lista_credito

    @property
    def extrato_banco(self) -> list:
        return self._extrato_banco

    @property
    def divida_emprestimo(self) -> float:
        return self._divida_emprestimo
    
    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=dados.get('id', 0),  # Valor padrão 0 se 'id' não existir
            nome=dados.get('nome', 'Sem Nome'),  # Valor padrão 'Sem Nome' se 'nome' não existir
            saldo_conta=dados.get('saldo_conta', 0.0),
            valor_anuidade=dados.get('valor_anuidade')  # Valor padrão 0.0 se 'saldo_conta' não existir
        )
    def extrato_credito(self, valor: float):
        self._lista_credito.append(valor)
        self._saldo_conta += valor
        self._extrato_banco.append(f'Creditos adicionados {valor}')

    def transferencia(self, destino: 'Correntista', valor: float):
        if self._saldo_conta >= valor:
            self._saldo_conta -= valor
            destino._saldo_conta += valor
            self._extrato_banco.append(f'transferencia para {destino.nome}: -{valor}')
            destino._extrato_banco.append(f'transferencia recebida de {self.nome}: +{valor}')
        else:
            print('saldo insuficiente para realizar a transferência.')
            return False

    def emprestimo(self, valor: float):
        self._saldo_conta += valor
        self._divida_emprestimo += valor
        self._extrato_banco.append(f'Emprestimo realizado: +{valor}')

    def atualizar_mes(self):
        if self._saldo_conta >= self._valor_anuidade:
            self._saldo_conta -= self._valor_anuidade
            self._extrato_banco.append(f'anuidade debitada: -{self._valor_anuidade}')
        else:
            print("Saldo insuficiente")

    def fatura(self, valor: float):
        if valor <= 0:
            print('pagamento deve ser positivo')
            return
        if self._saldo_conta >= valor:
            if valor > self._divida_emprestimo:
                valor = self._divida_emprestimo
            self._saldo_conta -= valor
            self._divida_emprestimo -= valor
            self._extrato_banco.append(f'Pagamento de fatura: -{valor}')
        else:
            print('saldo insuficiente para pagar a fatura')

    def __str__(self):
        return f"Correntista {self.nome} com saldo de R$ {self.saldo_conta:.2f}"

from datetime import datetime

class Transacao:
    def __init__(self, id_transacao: int, valor: float, tipo: str, pagador_id: int, beneficiario_id: int, data: str):
        self._id_transacao = id_transacao
        self._valor = valor
        self._tipo = tipo
        self._pagador_id = pagador_id
        self._beneficiario_id = beneficiario_id
        self._data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")  # Converte a string para um objeto datetime

    @property
    def id_transacao(self) -> int:
        return self._id_transacao

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def pagador_id(self) -> int:
        return self._pagador_id

    @property
    def beneficiario_id(self) -> int:
        return self._beneficiario_id

    @property
    def data(self) -> str:
        return self._data.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Transação do tipo {self.tipo} de R$ {self.valor:.2f} em {self.data}"

class Banco:
    def __init__(self, nome: str):
        self._nome = nome
        self._clientes = []
        self._investidor = []
        self._transacoes = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def clientes(self) -> List['Correntista']:
        return self._clientes

    @property
    def investidor(self) -> List['Investidor']:
        return self._investidor

    def adicionar_cliente(self, cliente: 'Correntista'):
        self._clientes.append(cliente)

    def adicionar_transacao(self, transacao: 'Transacao'):
        self._transacoes.append(transacao)

    def adicionar_Investidor(self, investidor: 'Investidor'):
        self._investidor.append(investidor)

    def salvar_dados(self, arquivo: str):
        dados = {
            'nome': self.nome,
            'clientes': [
                {
                    'id': c.id,
                    'nome': c.nome,
                    'valor_anuidade': c.valor_anuidade,
                    'saldo_conta': c.saldo_conta,
                    'divida_emprestimo': [
                        {
                            'id_emprestimo': e.id_emprestimo,  # Usando a propriedade
                            'valor_emprestimo': e.valor_emprestimo,  # Usando a propriedade
                            'numero_parcelas': e.numero_parcelas,  # Usando a propriedade
                            'data_emprestimo': e.data_emprestimo  # Usando a propriedade
                        }
                        for e in getattr(c, '_divida_emprestimo', []) if isinstance(e, Emprestimo)  # Verifica se 'e' é uma instância de Emprestimo
                    ]
                }
                for c in self._clientes
            ],
            'transacoes': [
                {
                    'id_transacao': t.id_transacao,
                    'tipo': t.tipo,
                    'valor': t.valor,
                    'pagador_id': t.pagador_id,
                    'beneficiario_id': t.beneficiario_id,
                    'data': t.data
                }
                for t in self._transacoes
            ],
            'investidor': [
                {
                    'id': i.id,
                    'nome': i.nome,
                    'saldo_conta': i.saldo_conta
                }
                for i in self._investidor
            ]
        }

        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=4)
    @classmethod
    def carregar_dados(cls, arquivo: str):
        try:
            with open(arquivo, 'r') as f:
                dados = json.load(f)
            return cls.from_dict(dados)
        except FileNotFoundError:
            return cls("Banco Sem Nome")
        except json.JSONDecodeError:
            return cls("Banco Sem Nome")

    @classmethod
    def from_dict(cls, dados: dict):
        banco = cls(dados.get('nome', 'Banco Sem Nome'))
        banco._clientes = [Correntista.from_dict(c) for c in dados.get('clientes', [])]
        banco._transacoes = dados.get('transacoes', [])
        banco._investidor = [Investidor.from_dict(i) for i in dados.get('investidor', [])]
        return banco

    def __str__(self):
        return f'Banco {self.nome} - Clientes: {len(self.clientes)} - Transações: {len(self._transacoes)}'

class Emprestimo:
    def __init__(self, id_emprestimo: int, valor_emprestimo: float, numero_parcelas: int, data_emprestimo: str,
                 correntista: 'Correntista'):
        self._id_emprestimo = id_emprestimo
        self._valor_emprestimo = valor_emprestimo
        self._numero_parcelas = numero_parcelas
        self._data_emprestimo = datetime.strptime(data_emprestimo, "%Y-%m-%d")
        self._valor_pago = 0.0
        self._valor_restante = valor_emprestimo
        self._lista_parcelas = self.calcular_parcela()
        self._correntista = correntista

    @property
    def id_emprestimo(self) -> int:
        return self._id_emprestimo
    
    @property
    def lista_parcelas(self) -> list:
        return self._lista_parcelas

    @property
    def valor_emprestimo(self) -> float:
        return self._valor_emprestimo

    @property
    def numero_parcelas(self) -> int:
        return self._numero_parcelas

    @property
    def data_emprestimo(self) -> str:
        return self._data_emprestimo.strftime("%Y-%m-%d")

    @property
    def correntista(self) -> 'Correntista':
        return self._correntista
    
    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id_emprestimo=dados['id_emprestimo'],
            valor_emprestimo=dados['valor_emprestimo'],
            numero_parcelas=dados['numero_parcelas'],
            data_emprestimo=dados['data_emprestimo'],
            correntista=None  
        )

    def calcular_parcela(self) -> list:
        taxa_juros = 0.05
        valor_parcela = (self._valor_emprestimo * taxa_juros) / (1-(1 + taxa_juros)** -self._numero_parcelas)
        return [{"numero": i + 1, "valor": valor_parcela, "paga": False} for i in range(self._numero_parcelas)]

    def pagar_mes(self):
        if self._valor_restante <= 0:
            print('Emprestimo já foi quitado')
            return
        for parcela in self._lista_parcelas:
            if not parcela['paga']:
                parcela['paga'] = True
                self._valor_pago += parcela['valor']
                self._valor_restante -= parcela['valor']
                print(f"Parcela {parcela['numero']} paga: {parcela['valor']}")
                break
        return False

    def amortizar_parcela_futura(self, valor: float):
        if self._valor_restante <= 0:
            print('O empréstimo já foi quitado')
            return

        if valor <= 0:
            print("O valor da amortização deve ser positivo.")
            return

        for parcela in self._lista_parcelas:
            if not parcela['paga']:
                if valor >= parcela['valor']:
                    valor -= parcela['valor']
                    parcela['paga'] = True
                    self._valor_pago += parcela['valor']
                    self._valor_restante -= parcela['valor']
                    print(f"Parcela {parcela['numero']} amortizada: {parcela['valor']}")
                else:
                    parcela['valor'] -= valor
                    self._valor_pago += valor
                    self._valor_restante -= valor
                    print(f"Parcela {parcela['numero']} amortizada parcialmente: {valor}")
                    break

    def pegar_valor(self) -> float:
        return self._valor_emprestimo

class Investidor(Correntista):
    def __init__(self, id: int, nome: str, valor_anuidade: float, saldo_conta: float):
        super().__init__(id,nome, valor_anuidade, saldo_conta)
        self._investimentos = []
        self._extrato_bancario = []

    @property
    def investimentos(self) -> list:
        return self._investimentos
    @property
    def extrato_bancario(self)-> list:
        return self._extrato_bancario
    
    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=dados.get('id', 0),
            nome=dados.get('nome', 'Sem Nome'), 
            saldo_conta=dados.get('saldo_conta', 0.0),
            valor_anuidade = dados.get('valor_anuidade',0.0)
        )

    def transferencia(self, destino: 'Investidor', valor: float):
        if self.saldo_conta >= valor:
            self.saldo_conta -= valor
            destino.saldo_conta += valor
            self.extrato_banco.append(f'Transferência efetuada com sucesso no valor de {valor}')
        else:
            print('Saldo insuficiente')

    def investimento(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do investimento deve ser positivo.")
        if self.saldo_conta < valor:
            raise ValueError("Saldo insuficiente para realizar o investimento.")
        
        self.saldo_conta -= valor  # Usando o setter para atualizar o saldo
        self._investimentos.append({"valor": valor, "descricao": "Investimento"})
        print(f"Investimento de R${valor:.2f} realizado com sucesso! Saldo atual: R${self.saldo_conta:.2f}")

    def atualizar_mes(self):
        if self.saldo_conta >= self.valor_anuidade:
            self.saldo_conta -= self.valor_anuidade
            self.extrato_banco.append(f'Debitado valor anual de {self.valor_anuidade}')
        else:
            print('Valor insuficiente')
            return False