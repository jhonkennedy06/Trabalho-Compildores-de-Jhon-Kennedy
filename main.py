# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (agosto-2024)
# ---------------------------------------------------
from lexico import Lexico
from sintatico import Sintatico


class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)
        self.sintatico = Sintatico(self.lexico)

    def traduz(self):
        self.sintatico.traduz()

    def testaLexico(self):
        self.sintatico.testaLexico()

    def finaliza(self):
        self.arq.close()


# inicia a traducao
if __name__ == '__main__':
    x = Tradutor('minipascal.txt')
    x.inicializa()
    #x.testaLexico()
    x.traduz()
    x.finaliza()
