from Lexer import Lexer
from Token import Token
from dict import *


inp = open("open.txt", 'r')
lexer = Lexer()
lexer.reserve(Token(RETURN, 'return'))
lexer.reserve(Token(DEF, "def"))
lookahead = lexer.scan(inp)


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
        print(lookahead.value)
        match(NUM)
    elif lookahead.tag == STRING:
        print(lookahead.value)
        match(STRING)
    else:
        raise SyntaxError


def return_expr():
    global lookahead
    if lookahead.tag == RETURN:
        #print(ASM_RETURN_STMT, end='')
        match(RETURN)
        print(f"mov eax {lookahead.value}\nret\n")
        const()
        match(NL)
    else:
        raise SyntaxError


def program():
    global lookahead
    if lookahead.tag == DEF:
        match(DEF)
        print(f"{lookahead.value} PROC")
        match(ID)
        match(LPAR)
        match(RPAR)
        match(COLON)
        match(NL)
        match(INDENT)
        return_expr()
        match(DEDENT)
        match(ENDMARK)
    else:
        raise SyntaxError
