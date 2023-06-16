import sys
import os
from Lexer import Lexer
from Token import Token
from dict import *

def_list = []
var_list = []
a = open("6-20-Python-IO-81-Rybnikov.txt", 'r')
input = a.read()
lexer = Lexer()
lexer.hold(Token(LOGAND, 'and'))
lexer.hold(Token(RETURN, 'return'))
lexer.hold(Token(DEF, "def"))
lexer.hold(Token(IF, 'if'))
lexer.hold(Token(ELSE, "else"))
lexer.hold(Token(WHILE, "while"))
unar_op_not = False
unar_op_inv = False


def match(a):
    global lookahead
    global input
    if lookahead.tag == a:
        lookahead = lexer.scan(input)
    else:
        raise SyntaxError


def term(t):
    global lookahead
    global unar_op_not, unar_op_inv
    if lookahead.tag == NUM:
        if unar_op_not:
            t = "\tmov ebx, " + str(lookahead.value) + "\n" + t
            t += "\tmov eax, ebx\n"
            match(NUM)
            unar_op_not = False
        elif unar_op_inv:
            t = "\tmov ebx, " + str(lookahead.value) + "\n" + t
            t += "\tmov eax, ebx\n"
            match(NUM)
            unar_op_inv = False
        else:
            t += str(lookahead.value) + "\n"
            match(NUM)
    elif lookahead.tag == LPAR:
        match(LPAR)
        t = expression(t)
        match(RPAR)
    elif lookahead.tag == UNAR_NOT:
        unar_op_not = True
        match(UNAR_NOT)
        if lookahead.value in var_list:
            match(ID)
            t += "\tcmp ecx, 0\n\tpushf\n\txor ecx, ecx\n\tpopf\n\tsetz cl\n"
            t = term(t)
        else:
            t += "\tcmp ecx, 0\n\tpushf\n\txor ecx, ecx\n\tpopf\n\tsetz cl\n"
            t = term(t)
    elif lookahead.tag == INV:
        unar_op_inv = True
        match(INV)
        if lookahead.value in var_list:
            match(ID)
            t += "\tnot eax\n"
            t = term(t)
        else:
            t += "\tnot ebx\n"
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
        t += "\tjmp _post_conditional\n"
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
            if lookahead.value in var_list:
                match(ID)
            else:
                print(f"Unknown variable in {str(lexer.line)} line, {str(lexer.error)} index")
                os.system("PAUSE")
                sys.exit(1)
            if lookahead.tag == LESS:
                match(LESS)
            if lookahead.tag == MORE:
                match(MORE)
            t += "\tmov ecx, "
            t = expression(t)
            t += "\tcycle:\n"
            try:
                match(COLON)
            except SyntaxError:
                print(f"SyntaxError in {str(lexer.line - 1)} line, {str(lexer.error + 9)} index. Expect \":\".")
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
                print(f"Unknown variable in {str(lexer.line)} line, {str(lexer.error)} index")
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


def start(c):
    global lookahead
    inside = []
    outside = []
    outside_s = ''
    inside_s = ''
    counter_of_names = 0
    counter_in = 0
    counter_out = 0
    lookahead = lexer.scan(input)
    while lookahead.tag != ENDMARK:
        while lookahead.tag == DEF:
            counter_out += 1
            match(DEF)
            invoker = ''
            invoker += f"\n{lookahead.value} proc\n"
            def_list.append(lookahead.value)
            match(ID)
            match(LPAR)
            match(RPAR)
            match(COLON)
            match(NL)
            match(INDENT)
            invoker += expression()
            if def_list[counter_of_names] != "main":
                invoker += f"\tinvoke MessageBox,0,str$(eax), ADDR Caption, MB_OK\n"
            if def_list[counter_of_names] == "main":
                invoker += f"\tcall {def_list[counter_of_names-1]}\n"
            invoker += f"\tret\n"
            while lookahead.tag == DEDENT:
                match(DEDENT)
            invoker += f"{def_list[counter_of_names]} endp\n"
            counter_of_names += 1
            while lookahead.tag == NL:
                match(NL)
            outside.append(invoker)
        while lookahead.tag == ID:
            invoker = ''
            counter_in += 1
            if lookahead.value in def_list:
                invoker += f"\tinvoke {lookahead.value}\n"
                match(ID)
                match(LPAR)
                match(RPAR)
                while lookahead.tag == NL:
                    match(NL)
            else:
                invoker = expression(invoker)
            inside.append(invoker)
    match(ENDMARK)
    for i in range(counter_out):
        outside_s += outside[i]
    for j in range(counter_in):
        inside_s += inside[j]
    c = c + outside_s + "\nstart:\n" + inside_s + "\tinvoke ExitProcess, 0\nend start"
    return c
