import sys
import os
from Lexer import Lexer
from Token import Token
from dict import *

def_list = []
var_list = []
a = open("RGR-20-Python-IO-81-Rybnikov.txt", 'r')
input = a.read()
lexer = Lexer()
lexer.hold(Token(LOGAND, 'and'))
lexer.hold(Token(RETURN, 'return'))
lexer.hold(Token(DEF, "def"))
lexer.hold(Token(IF, 'if'))
lexer.hold(Token(ELSE, "else"))
lexer.hold(Token(WHILE, "while"))
flag_unarop = False


def match(a):
    global lookahead
    global input
    if lookahead.tag == a:
        lookahead = lexer.scan(input)
        print(lookahead)
    else:
        raise SyntaxError


def term(t):
    global lookahead
    global flag_unarop
    if lookahead.tag == NUM:
        if flag_unarop:
            t = "\tmov ebx, " + str(lookahead.value) + "\n" + t
            t += "\tmov eax, ebx\n"
            match(NUM)
            flag_unarop = False
        else:
            t += str(lookahead.value) + "\n"
            match(NUM)
    elif lookahead.tag == LPAR:
        match(LPAR)
        t = expression(t)
        match(RPAR)
    elif lookahead.tag == UNAR_NOT:
        flag_unarop = True
        match(UNAR_NOT)
        if lookahead.value in var_list:
            match(ID)
            t += "\tcmp ecx, 0\n\tpushf\n\txor ecx, ecx\n\tpopf\n\tsetz cl\n"
            t = term(t)
        else:
            t += "\tcmp ecx, 0\n\tpushf\n\txor ecx, ecx\n\tpopf\n\tsetz cl\n"
            t = term(t)
    while lookahead.tag == STRING:
        print("Type error: Expected int, got String in " + str(lexer.line) + " line, " + str(lexer.error) +
              " index")
        os.system("PAUSE")
        sys.exit(1)
    return t


def expression(t = ""):
    global lookahead
    counter = 0
    t = term(t)
    if lookahead.tag == PLUS:
        while lookahead.tag == PLUS:
            match(PLUS)
            if lookahead.value in var_list:
                t += "\tadd eax, ebp\n"
                t = expression(t)
            else:
                t += "\tadd eax, "
                t = expression(t)
    elif lookahead.tag == MINUS:
        while lookahead.tag == MINUS:
            match(MINUS)
            t += "\tsub eax, "
            t = expression(t)
    elif lookahead.tag == MULT:
        while lookahead.tag == MULT:
            match(MULT)
            t += "\tmov ebx, "
            t = expression(t)
            t += "\tmul ebx\n"
    elif lookahead.tag == LOGAND:
        while lookahead.tag == LOGAND:
            match(LOGAND)
            t += "\tcmp eax, 0\n" \
                 "\tjne _case2\n" \
                 "\tjmp _end\n"
            t += "_case2:\n" \
                 "\tmov eax, "
            t = expression(t)
            t += "\tcmp eax, 0\n" \
                 "\tmov eax, 0\n" \
                 "\tsetne al\n" \
                 "_end:\n"
            t = expression(t)
    elif lookahead.tag == ID:
        var_list.append(lookahead.value)
        match(ID)
        if lookahead.tag == MINUS:
            if lookahead.tag != EQUAL:
                match(MINUS)
                t += "\tsub eax, "
                t = expression(t)
                match(EQUAL)
                t += ""
                t = expression(t)
                t += ""
                t = expression(t)
        if lookahead.tag == PLUS:
            if lookahead.tag != EQUAL:
                match(PLUS)
                t += "\tadd eax, "
                t = expression(t)
                match(EQUAL)
                t += ""
                t = expression(t)
                t += ""
                t = expression(t)
        if counter < 1:
            if lookahead.tag == EQUAL:
                counter += 1
                match(EQUAL)
                t += "\tpush ebp\n" \
                     "\tmov ebp, esp\n" \
                     "\tmov eax, "
                t = expression(t)
                t += "\tpush eax \n" \
                     "\tmov esp, ebp\n" \
                     "\tpop ebp\n"
                t = expression(t)
    elif lookahead.tag == IF:
        match(IF)
        t += "" \
             "\tjmp _post_conditional\n"
        t = expression(t)
        if lookahead.tag == ELSE:
            match(ELSE)
            t += "\t_e2:\n" \
                 "\tmov eax, "
            t = expression(t)
            t += "\t_post_conditional:\n"
    elif lookahead.tag == WHILE:
        while lookahead.tag == WHILE:
            match(WHILE)
            match(ID)
            if lookahead.tag == LESS:
                match(LESS)
            if lookahead.tag == MORE:
                match(MORE)
            t += "\tmov ecx, "
            t = expression(t)
            t += "\tcycle:\n"
            match(COLON)
            match(NL)
            match(INDENT)
            t = expression(t)
            t += "\tcmp eax, ecx\n" \
                 "\tjne cycle\n"
    elif lookahead.tag == RETURN:
        match(RETURN)
        if lookahead.tag != UNAR_NOT and lookahead.tag != ID:
            t += "\tmov eax, "
        if lookahead.value in var_list:
            match(ID)
        if lookahead.tag == ID and lookahead.value not in var_list:
            if lookahead.value not in def_list:
                print("Unknown variable in " + str(lexer.error) + " line, " + str(
                    lexer.error) + " index")
                os.system("PAUSE")
                sys.exit(1)
        if lookahead.value in def_list:
            match(ID)
            match(LPAR)
            match(RPAR)
        if lookahead.tag == ID and lookahead.value not in def_list:
            print("Unknown function call in " + str(lexer.line) + " line, " + str(
                lexer.error) + " index")
            os.system("PAUSE")
            sys.exit(1)
        t = expression(t)
        while lookahead.tag == NL:
            match(NL)
    while lookahead.tag == NL:
        match(NL)
        if lookahead.tag == DEDENT:
            match(DEDENT)
    return t


def start():
    global lookahead
    lookahead = lexer.scan(input)
    try:
        match(DEF)
        invoker = ''
        invoker += f"\n{lookahead.value} proc\n"
        def_list.append(lookahead.value)
        match(ID)
        match(LPAR)
        match(RPAR)
        match(COLON)
        while lookahead.tag == NL:
            match(NL)
        match(INDENT)
        var_list.append(lookahead.value)
        match(ID)
        match(EQUAL)
        invoker += f"\tmov eax, {lookahead.value}\n"
        match(NUM)
        while lookahead.tag == NL:
            match(NL)
        var_list.append(lookahead.value)
        match(ID)
        match(EQUAL)
        invoker += f"\tmov ebx, {lookahead.value}\n"
        match(NUM)
        while lookahead.tag == NL:
            match(NL)
        var_list.append(lookahead.value)
        match(ID)
        match(EQUAL)
        invoker += f"\tmov ecx, {lookahead.value}\n"
        match(NUM)
        while lookahead.tag == NL:
            match(NL)
        var_list.append(lookahead.value)
        match(ID)
        match(EQUAL)
        invoker += f"\tmov edx, {lookahead.value}\n"
        match(NUM)
        while lookahead.tag == NL:
            match(NL)
        match(WHILE)
        if lookahead.value == var_list[3]:
            match(ID)
        else:
            raise SyntaxError
        match(MORE)
        match(NUM)
        match(COLON)
        #match(INDENT)
        while lookahead.tag == NL:
            match(NL)
        match(INDENT)
        if lookahead.value == var_list[2]:
            match(ID)
        else:
            raise SyntaxError
        match(EQUAL)
        if lookahead.value == var_list[0]:
            match(ID)
        else:
            raise SyntaxError
        match(PLUS)
        if lookahead.value == var_list[1]:
            match(ID)
        else:
            raise SyntaxError
        while lookahead.tag == NL:
            match(NL)
        if lookahead.value == var_list[1]:
            match(ID)
        else:
            raise SyntaxError
        match(EQUAL)
        if lookahead.value == var_list[0]:
            match(ID)
        else:
            raise SyntaxError
        while lookahead.tag == NL:
            match(NL)
        if lookahead.value == var_list[0]:
            match(ID)
        else:
            raise SyntaxError
        match(EQUAL)
        if lookahead.value == var_list[2]:
            match(ID)
        else:
            raise SyntaxError
        while lookahead.tag == NL:
            match(NL)
        if lookahead.value == var_list[3]:
            match(ID)
        else:
            raise SyntaxError
        match(EQUAL)
        if lookahead.value == var_list[3]:
            match(ID)
        else:
            raise SyntaxError
        match(MINUS)
        match(NUM)
        while lookahead.tag == NL:
            match(NL)
        match(DEDENT)
        invoker += f"\n\tcycle:" \
                   f"\n\tsub edx, 1" \
                   f"\n\tadd ecx, ebx" \
                   f"\n\tmov ebx, eax" \
                   f"\n\tmov eax, ecx" \
                   f"\n\tcmp edx, 1" \
                   f"\n\tjne cycle\n" \
                   f"\n\tfn MessageBox,0,str$(ecx),\"Rybnikov\",MB_OK" \
                   f"\n\tret" \
                   f"\n{def_list[0]} endp"
        match(RETURN)
        if lookahead.value == var_list[2]:
            match(ID)
        else:
            raise SyntaxError
        while lookahead.tag == NL:
            match(NL)
        while lookahead.tag == DEDENT:
            match(DEDENT)
        while lookahead.tag == NL:
            match(NL)
        invoker += f"\nstart:" \
                   f"\n\tinvoke {def_list[0]}" \
                   f"\n\tinvoke ExitProcess, 0" \
                   f"\nend start"
        if lookahead.value == def_list[0]:
            match(ID)
        else:
            raise SyntaxError
        match(LPAR)
        match(RPAR)
        return invoker
    except SyntaxError:
        print(f"Syntax Error in line {lexer.line}, {lexer.error}")
