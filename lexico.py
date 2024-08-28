# ---------------------------------------------------
# Tradutor para a linguagem CALC
#
# versao 1a (mar-2024)
# ---------------------------------------------------
from ttoken import TOKEN


class Lexico:
    # -------------------------------------------------------------------------------------------------------

    def __init__(self, arqFonte):
        self.arqFonte = arqFonte  # objeto file
        self.fonte = self.arqFonte.read()  # string contendo file
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None  # (token, lexema, linha, coluna)
        self.linha = 1  # linha atual no fonte
        self.coluna = 0  # coluna atual no fonte

    # -------------------------------------------------------------------------------------------------------

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    # -------------------------------------------------------------------------------------------------------

    def getchar(self):
        if self.fimDoArquivo():
            return '\0'
        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
        if car == '\n':
            self.linha += 1
            # colocar self.coluna = 1 também está funcionando, ver qual dos dois está realmente certo
            self.coluna = 0
        else:
            self.coluna += 1
        return car

    # -------------------------------------------------------------------------------------------------------

    def ungetchar(self, simbolo):
        if simbolo != '\0':
            if simbolo == '\n':
                self.linha -= 1

            if self.indiceFonte > 0:
                self.indiceFonte -= 1

            self.coluna -= 1
        else:
            pass

    # -------------------------------------------------------------------------------------------------------

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    # -------------------------------------------------------------------------------------------------------

    def getToken(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''
        while simbolo in ['/', ' ', '\t', '\n']:
            # descarta comentarios (que iniciam com # ate o fim da linha)
            if simbolo == '/':  # DEFINIMOS COMENTÁRIOS COMO /
                simbolo = self.getchar()
                if simbolo == '/':  # DEFINIMOS COMENTÁRIOS COMO /
                    while simbolo != '\n':
                        simbolo = self.getchar()

                else:
                    self.ungetchar(simbolo)
                    simbolo = '/'
                    break
            # descarta linhas brancas e espaços
            while simbolo in [' ', '\t', '\n']:
                simbolo = self.getchar()
        # aqui vai começar a pegar um token...
        lin = self.linha  # onde inicia o token, para msgs
        col = self.coluna  # onde inicia o token, para msgs
        while (True):
            if estado == 1:
                # inicio do automato
                if simbolo.isalpha():  # estado para identificadores e palavras reservadas
                    estado = 2
                # **********************************
                elif simbolo.isdigit():  # estado para achar numeros
                    estado = 3
                # **********************************
                elif simbolo == '"':  # estado para achar strings
                    estado = 4
                # **********************************
                elif simbolo == "<":  # verifica se é sinal de menor ou menor igual
                    estado = 5  # < ou <=
                # **********************************
                elif simbolo == ">":  # verifica se é sinal de maior ou maior igual > ou >=
                    estado = 6  # > ou >=
                # **********************************
                elif simbolo == ":":
                    estado = 7  # :-
                # **********************************
                elif simbolo == ".":  # se for ponto vai para o estado 8
                    estado = 8
                # **********************************
                elif simbolo == "=":
                    return (TOKEN.relop, "=", lin, col)
                # **********************************
                elif simbolo == "(":
                    return (TOKEN.abreParentese, "(", lin, col)
                # **********************************
                elif simbolo == ")":
                    return (TOKEN.fechaParentese, ")", lin, col)
                # **********************************
                elif simbolo == ",":
                    return (TOKEN.virgula, ",", lin, col)
                # **********************************
                elif simbolo == ";":
                    return (TOKEN.pontoVirgula, ";", lin, col)
                # **********************************
                elif simbolo == "+":
                    return (TOKEN.addop, "+", lin, col)
                # **********************************
                elif simbolo == "-":
                    return (TOKEN.addop, "-", lin, col)
                # **********************************
                elif simbolo == "*":
                    return (TOKEN.mulop, "*", lin, col)
                # **********************************
                elif simbolo == "/":
                    return (TOKEN.mulop, "/", lin, col)
                # **********************************
                elif simbolo == "[":
                    return (TOKEN.abreColchete, "[", lin, col)
                # **********************************
                elif simbolo == "]":
                    return (TOKEN.fechaColchete, "]", lin, col)
                # **********************************
                elif simbolo == '\0':
                    return (TOKEN.eof, '<eof>', lin, col)
                # **********************************
                else:
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)

            # -------------------------------------------------------------------------------------------------------

            elif estado == 2:
                # identificadores e palavras reservadas
                if simbolo.isalnum():  # se for numero ou letra ele fica lendo até tentar achar a palavra reservada
                    estado = 2
                # **********************************
                else:  # se não for numero ou letra ele retorna a palavra reservada
                    self.ungetchar(simbolo)  # deslê
                    token = TOKEN.reservada(lexema)  # guarda a palavra reservada
                    return (token, lexema, lin, col)

            # -------------------------------------------------------------------------------------------------------
            elif estado == 3:  # estado para achar o numerop
                # numeros
                if simbolo.isdigit():  # se for numero, ele retorna ao estado
                    estado = 3
                # **********************************
                elif simbolo == '.':  # se for ponto, ele entra na parte do real
                    proximo = self.getchar()
                    self.ungetchar(simbolo)
                    if proximo == '.':
                        self.ungetchar(simbolo)
                        return (TOKEN.numeroInteiro, lexema, lin, col)
                    else:
                        estado = 31
                # **********************************
                elif simbolo.isalpha():  # se for letra, erro
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)
                # **********************************
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.numeroInteiro, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 31:  # verifica a parte real do numero
                # parte real do numero
                if simbolo.isdigit():  # se for numero, ele vai para o estado 32 para começar pegar a parte real
                    estado = 32
                # **********************************
                else:  # se NÃO for numero, erro
                    self.ungetchar(simbolo)
                    return (TOKEN.erro, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 32:  # consome parte real do numero
                # parte real do numero
                if simbolo.isdigit():  # se for numero ele continua lendo
                    estado = 32
                elif simbolo.isalpha():  # se NÃO for numero, erro
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)
                else:  # se NÃO for numero e nem letra, ele retorna o numero real
                    self.ungetchar(simbolo)
                    return (TOKEN.numeroReal, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 4:  # estado para achar strings
                # strings
                while True:
                    if simbolo == '"':  # se achar outra aspa é pq ele encontrou o final da string
                        lexema += simbolo
                        return (TOKEN.string, lexema, lin, col)

                    if simbolo in ['\n', '\0']:  # se for "final de arquivo" ou "pular linha" sem fechar a aspa, erro
                        return (TOKEN.erro, lexema, lin, col)

                    if simbolo == '\\':  # isso é por causa do python, verifica se o caractere atual é uma barra invertida para caracter especial
                        lexema += simbolo
                        simbolo = self.getchar()
                        if simbolo in ['\n',
                                       '\0']:  # se for final de arquivo ou ele pular a linha sem fechar a aspa, erro
                            return (TOKEN.erro, lexema, lin, col)

                    lexema = lexema + simbolo  # aqui ele concatena com a string enquanto não acha o final da string
                    simbolo = self.getchar()  # aqui ele vai lendo o proximo caracter
            # -------------------------------------------------------------------------------------------------------

            elif estado == 5:  # verifica se é sinal de diferente  menor ou menor igual  # <> ou < ou <=

                if simbolo == '>':  # se encontrar o ">" é pq ele é o diferente
                    lexema = lexema + simbolo
                    return (TOKEN.relop, lexema, lin, col)

                elif simbolo == '=':  # se encontrar o "=" é pq ele é menor igual
                    lexema = lexema + simbolo
                    return (TOKEN.relop, lexema, lin, col)

                else:  # se não encontrar é pq ele é apenas o menor
                    self.ungetchar(simbolo)
                    return (TOKEN.relop, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 6:  # verifica se é sinal de maior ou maior igual > ou >=
                if simbolo == '=':  # se encontrar o "=" é pq ele é menor igual
                    lexema = lexema + simbolo
                    return (TOKEN.relop, lexema, lin, col)
                else:  # se não encontrar é pq ele é apenas o maior
                    self.ungetchar(simbolo)
                    return (TOKEN.relop, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 7:  # sinal de atribuição ou 2 pontos :-
                if simbolo == '=':  # é igual ao assingop  :-
                    lexema += simbolo
                    return (TOKEN.assignop, lexema, lin, col)
                else:  # se nao tiver o = é pq é só o dois ponto
                    self.ungetchar(simbolo)
                    return (TOKEN.doisPontos, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            elif estado == 8:  # se for ponto entra aqui
                if simbolo == '.':  # se for ponto 2 vezes é pq ele é o ponto ponto do array
                    lexema += simbolo
                    return (TOKEN.pontoPonto, lexema, lin, col)
                else:  # se o proximo simbolo nao for '..' é pq é apenas um ponto
                    return (TOKEN.ponto, lexema, lin, col)
            # -------------------------------------------------------------------------------------------------------

            else:
                print('BUG!!!')

            lexema = lexema + simbolo
            simbolo = self.getchar()

    def testaLexico(self):
        self.tokenLido = self.getToken()
        (token, lexema, linha, coluna) = self.tokenLido

        while token != TOKEN.eof:
            self.imprimeToken(self.tokenLido)
            self.tokenLido = self.getToken()
            (token, lexema, linha, coluna) = self.tokenLido
        self.imprimeToken(self.tokenLido)  # serve apenas para mostrar que o arquivo acabou


# inicia a traducao
if __name__ == '__main__':
    print("Para testar, chame o Tradutor no main.py")
    x = Lexico('minipascal.txt')

    x.testaLexico()
