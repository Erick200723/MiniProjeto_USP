import json
import os

class Tarefas:
    def __init__(self,descricao, status=False):
        self.descricao = descricao
        self.status = status

    def to_dic(self):
        return{
            "descrição": self.descricao,
            "status": self.status
        }


# Classe que vai gerenciar as tarefas
# Vai ter os métodos de adicionar, remover, listar e alterar tarefas
# Explorar recursos de classes como class abstract e polimorfismo e herança para criar classes de tarefas
# Vai ter um método para salvar as tarefas em um arquivo json
# vai ter um método para carregar as tarefas de um arquivo json
class GerenciadorTrafeas:
    pass

logica = GerenciadorTrafeas()