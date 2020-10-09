from Lexer import Lexer
from Token import Token
from dict import *

list_of_names_def = []
list_of_names_var = []
a = open("1-20-Python-IO-81-Rybnikov.txt", 'r')
inp = a.read()
lexer = Lexer()
lexer.reserve(Token(RETURN, 'return'))
lexer.reserve(Token(DEF, "def"))
unar_flag = False


def match(l):
    global lookahead
    global inp
    if lookahead.tag == l:
        print(f"{lookahead.tag}: {lookahead.value}")
        lookahead = lexer.scan(inp)
    else:
        raise SyntaxError(lexer.line + " line")


def term(t):
    global lookahead
    global unar_flag
    global function_call
    if lookahead.tag == NUM:
        if unar_flag:
            t = "\tmov ecx, " + str(lookahead.value) + "\n" + t
            t += "\tmov eax, ecx\n"
            match(NUM)
            unar_flag = False
        else:
            t += str(lookahead.value) + "\n"
            match(NUM)
    elif lookahead.tag == LPAR:
        match(LPAR)
        t = expr(t)
        match(RPAR)
    elif lookahead.tag == UNAR_NOT:
        unar_flag = True
        match(UNAR_NOT)
        t += "\tcmp ecx, 0\n\tpushf\n\txor ecx, ecx\n\tpopf\n\tsetz cl\n"
        t = term(t)
    return t


def expr(t = ""):
    global lookahead
    t = term(t)
    if lookahead.tag == PLUS:
        while lookahead.tag == PLUS:
            match(PLUS)
            t += "\tadd eax, "
            t = expr(t)
    elif lookahead.tag == ID:
        list_of_names_var.append(lookahead.value)
        match(ID)
        if lookahead.tag == EQUAL:
            match(EQUAL)
            t = expr(t)
    elif lookahead.tag == RETURN:
        match(RETURN)
        if lookahead.tag != UNAR_NOT:
            t += "\tmov eax, "
        t = expr(t)
        t += '\tfn MessageBox,0,str$(eax),"Rybnikov",MB_OK\n'
        t += "\tret\n"
        while lookahead.tag == NL:
            match(NL)
    while lookahead.tag == NL:
        match(NL)
    return t


def program(s):
    global lookahead
    inside = []
    inside_s = ''
    outside = []
    outside_s = ''
    counter_out = 0
    counter_in = 0
    counter_of_names = 0
    lookahead = lexer.scan(inp)
    while lookahead.tag != ENDMARK:
        while lookahead.tag == DEF:
            counter_out += 1
            match(DEF)
            debuger = ''
            debuger += f"\n{lookahead.value} PROC\n"
            list_of_names_def.append(lookahead.value)
            match(ID)
            match(LPAR)
            match(RPAR)
            match(COLON)
            match(NL)
            match(INDENT)
            debuger += expr()
            while lookahead.tag == DEDENT:
                match(DEDENT)
            debuger += f"{list_of_names_def[counter_of_names]} ENDP\n"
            counter_of_names += 1
            while lookahead.tag == NL:
                match(NL)
            outside.append(debuger)
        while lookahead.tag == ID:
            debuger = ''
            counter_in += 1
            if lookahead.value in list_of_names_def:
                debuger += f"\tinvoke {lookahead.value}\n"
                match(ID)
                match(LPAR)
                match(RPAR)
                while lookahead.tag == NL:
                    match(NL)
            else:
                debuger = expr(debuger)
            inside.append(debuger)
    match(ENDMARK)
    for i in range(counter_out):
        outside_s += outside[i]
    for i in range(counter_in):
        inside_s += inside[i]
    s = s + outside_s + "\nstart:\n" + inside_s + "\tinvoke ExitProcess, 0\nend start"
    # print(lexer.words)
    return s
