from Lexer import Lexer
from Token import Token
from dict import *

list_of_names = []
a = open("1-20-Python-IO-81-Rybnikov.txt", 'r')
inp = a.read()
lexer = Lexer()
lexer.reserve(Token(RETURN, 'return'))
lexer.reserve(Token(DEF, "def"))



def match(l):
    global lookahead
    global inp
    if lookahead.tag == l:
        lookahead = lexer.scan(inp)
    else:
        raise SyntaxError


def const():
    global lookahead
    if lookahead.tag == NUM:
        #print(lookahead.value)
        match(NUM)
    elif lookahead.tag == STRING:
        #print(lookahead.value)
        #match(STRING)
        raise TypeError("Get String but expected integer")
    else:
        raise SyntaxError


def return_expr(s):
    global lookahead
    if lookahead.tag == RETURN:
        match(RETURN)
        s += f"\t\tmov eax, {lookahead.value}\n\t\tret\n"
        const()
        while lookahead.tag == NL:
            match(NL)
        return s
    else:
        raise SyntaxError


def program(s):
    global lookahead
    lookahead = lexer.scan(inp)
    while lookahead.tag == DEF:
        if lookahead.tag == DEF:
            match(DEF)
            s += f"\t{lookahead.value} PROC\n"
            list_of_names.append(lookahead.value)
            match(ID)
            match(LPAR)
            match(RPAR)
            match(COLON)
            match(NL)
            match(INDENT)
            s = return_expr(s)
            while lookahead.tag == DEDENT:
                match(DEDENT)
            s += f"\t{list_of_names[0]} ENDP\n"
            while lookahead.tag == NL:
                match(NL)
        else:
            raise SyntaxError
    match(ENDMARK)
    return s