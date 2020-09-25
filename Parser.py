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
        print(f"{lookahead.tag}: {lookahead.value}")
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
        s += f"\tmov eax, {lookahead.value}\n\tret\n"
        const()
        while lookahead.tag == NL:
            match(NL)
        return s
    else:
        raise SyntaxError


def program(s):
    global lookahead
    counter_of_names = 0
    function_call = '\n_start:\n'
    lookahead = lexer.scan(inp)
    while lookahead.tag != ENDMARK:
        while lookahead.tag == DEF:
            match(DEF)
            s += f"\n{lookahead.value} PROC\n"
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
            s += f"{list_of_names[counter_of_names]} ENDP\n"
            counter_of_names += 1
            while lookahead.tag == NL:
                match(NL)
        while lookahead.tag == ID:
            if lookahead.value in list_of_names:
                function_call += f"\tinvoke {lookahead.value}\n"
                match(ID)
                match(LPAR)
                match(RPAR)
                while lookahead.tag == NL:
                    match(NL)
            else:
                raise SyntaxError("No such function")
    match(ENDMARK)
    s += function_call + "\tinvoke ExitProcess, 0"
    #print(lexer.words)
    return s
