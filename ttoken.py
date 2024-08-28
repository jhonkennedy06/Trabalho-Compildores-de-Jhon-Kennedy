# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (agosto-2024)
# ---------------------------------------------------

from enum import IntEnum


class TOKEN(IntEnum):
    PROGRAM = 1
    id = 2
    abreParentese = 3
    fechaParentese = 4
    pontoVirgula = 5
    ponto = 6
    virgula = 7
    VAR = 8
    doisPontos = 9
    ARRAY = 10
    numeroReal = 11
    numeroInteiro = 12
    OF = 13
    FUNCTION = 14
    PROCEDURE = 15
    BEGIN = 16
    END = 17
    assignop = 18  # atrib atribução
    WHILE = 19
    DO = 20
    IF = 21
    THEN = 22
    ELSE = 23
    abreColchete = 24
    fechaColchete = 25
    relop = 26  # operador relacional (>, <, >=, <=, =, <>)
    addop = 27  # soma e subtração (+ e -)
    mulop = 28  # multiplicação (*), divisão (/), div e mod
    NOT = 29
    eof = 30
    erro = 31
    INTEGER = 32
    REAL = 33
    pontoPonto = 34
    string = 35
    WRITELN = 36
    WRITE = 37
    READLN = 38
    READ = 39
    RETURN = 40

    @classmethod
    def msg(cls, token):
        nomes = {
            1: 'program',
            2: 'ident',
            3: '(',
            4: ')',
            5: ';',
            6: '.',
            7: ',',
            8: 'var',
            9: ':',
            10: 'array',
            11: 'número real',
            12: 'número inteiro',
            13: 'of',
            14: 'function',
            15: 'procedure',
            16: 'begin',
            17: 'end',
            18: ':=',
            19: 'while',
            20: 'do',
            21: 'if',
            22: 'then',
            23: 'else',
            24: '[',
            25: ']',
            26: 'operador relacional',
            27: 'operador adicional',
            28: 'operador multiplicacional',
            29: 'not',
            30: '<eof>',
            31: '***********.............ERROOOOOOO...........***********',
            32: 'inteiro',
            33: 'real',
            34: '..',
            35: 'string',
            36: 'writeln',
            37: 'write',
            38: 'readln',
            39: 'read',
            40: 'return'
        }
        return nomes[token]

    @classmethod  # metodo para palavras reservadas
    def reservada(cls, lexema):
        reservadas = {
            'program': TOKEN.PROGRAM,
            'var': TOKEN.VAR,
            'array': TOKEN.ARRAY,
            'of': TOKEN.OF,
            'function': TOKEN.FUNCTION,
            'procedure': TOKEN.PROCEDURE,
            'begin': TOKEN.BEGIN,
            'end': TOKEN.END,
            'while': TOKEN.WHILE,
            'do': TOKEN.DO,
            'if': TOKEN.IF,
            'then': TOKEN.THEN,
            'else': TOKEN.ELSE,
            'not': TOKEN.NOT,
            'integer': TOKEN.INTEGER,
            'real': TOKEN.REAL,
            'div': TOKEN.mulop,
            'mod': TOKEN.mulop,
            'writeln': TOKEN.WRITELN,
            'write': TOKEN.WRITE,
            'readln': TOKEN.READLN,
            'read': TOKEN.READ,
            'return': TOKEN.RETURN
        }
        # aqui ele verifica se a string lida é reservada
        if lexema in reservadas:  # se for reservada ele retorna o token referente
            return reservadas[lexema]
        else:  # se não for reservada, ele acha um identificador
            return TOKEN.id
