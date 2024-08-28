# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (agosto-2024)
# ---------------------------------------------------
from ttoken import TOKEN


class Semantico:

    def __init__(self, sintatico):
        self.sintatico = sintatico
        self.tabelaSimbolos = dict()
        self.alvo = open(self.sintatico.nomeAlvo, "wt")
        self.subrotinaAtual = 'program'


    def finaliza(self):
        self.alvo.close()

    def erroSemantico(self, msg):
        (token, lexema, linha, coluna) = self.sintatico.tokenLido
        print(f'Erro na linha {linha}: ')
        print(f' {msg}')
        raise Exception

    def gera(self, nivel, codigo):
        identacao = ' ' * 4 * nivel
        linha = identacao + codigo
        self.alvo.write(linha)

    # pega os identificadores e seu respectivo tipo e salva na tabela de símbolos
    # pega os identificadores e seu respectivo tipo e salva na tabela de símbolos
    def declara(self, nomes, tipo):  # tipo será uma string

        for id in nomes:
            if self.existe_id(id):
                msg = f'Identificador {id} ja existente'
                self.erroSemantico(msg)
            else:
                if self.subrotinaAtual == 'program':
                    if tipo == TOKEN.FUNCTION or tipo == TOKEN.PROCEDURE:
                        tab_funcao = dict()
                        self.tabelaSimbolos[id] = (tipo, tab_funcao)
                        self.entrou_subrotina(id)
                    else:
                        self.tabelaSimbolos[id] = (tipo, None)
                else:
                    nome = self.subrotinaAtual
                    (tipo_rotina, tabela) = self.tabelaSimbolos[nome]
                    tabela[id] = (tipo, None)

    def existe_id(self, identificador):
        if self.subrotinaAtual != 'program':
            nome = self.subrotinaAtual
            if nome in self.tabelaSimbolos:
                (tipo_rotina, tabela) = self.tabelaSimbolos[nome]
                if identificador in tabela:
                    return True
                else:
                    return False
            else:
                return identificador in self.tabelaSimbolos

        if identificador in self.tabelaSimbolos:
            return True
        else:
            return False

        # verifica o que é o identificador que eu passei (se é variavel, funcao, procedimento, etc.)

    def consulta_tipo_id(self, id):
        if self.subrotinaAtual != 'program':
            nome = self.subrotinaAtual
            (tipo_rotina, tabela) = self.tabelaSimbolos[nome]
            if id in tabela:
                return tabela[id]
        else:
            return self.tabelaSimbolos[id]

    def entrou_subrotina(self, nome):
        self.subrotinaAtual = nome

    def saiu_subrotina(self):
        self.subrotinaAtual = 'program'
