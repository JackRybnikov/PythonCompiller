from Token import Token
from dict import *


def is_hex(a):
    set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
    if a in set:
        return True
    else:
        return False


class Lexer():
    def __init__(self):
        self.line = 1
        self.index = 0
        self.error = 0
        self.peek = ' '
        self.words = {}
        self.indent = 0
        self.old_indent = 0
        self.spaces = 0

    def hold(self, t):
        self.words[t.value] = t

    def scan(self, content):
        if self.index == len(content):
            if self.old_indent != 0:
                self.old_indent -= 1
                return Token(DEDENT)
            return Token(ENDMARK)
        self.peek = content[self.index]

        while self.peek == '\t':
            self.indent += 1
            self.index += 1
            self.error += 1
            self.peek = content[self.index]

        while self.index < len(content) - 1:
            if self.peek == ' ':
                self.index += 1
                self.error += 1
                self.spaces += 1
                self.peek = content[self.index]
            else:
                self.indent += self.spaces // 4
                self.spaces = 0
                break

        if self.old_indent < self.indent:
            self.old_indent += 1
            return Token(INDENT)
        elif self.old_indent > self.indent:
            self.old_indent -= 1
            return Token(DEDENT)

        if self.peek == '"' or self.peek == "'":
            a = ''
            condition = True
            while condition:
                a += self.peek
                self.index += 1
                self.error += 1
                self.peek = content[self.index]
                condition = (self.peek != '"' and self.peek != "'")
                if self.index == len(content) - 1:
                    break
            a += self.peek
            self.index += 1
            self.error += 1
            self.peek = content[self.index]
            return Token(STRING, a)

        if self.peek == "\n":
            self.index += 1
            self.error = 0
            self.line += 1
            self.indent = 0
            return Token(NL)

        if self.peek.isdigit():
            k = 0
            cond = True
            if self.peek == '0':
                self.index += 1
                self.error += 1
                self.peek = content[self.index]
                if self.peek == 'x':
                    s = ''
                    self.index += 1
                    self.error += 1
                    self.peek = content[self.index]
                    while cond:
                        s += self.peek
                        if self.index == len(content) - 1:
                            break
                        self.index += 1
                        self.error += 1
                        self.peek = content[self.index]
                        cond = is_hex(self.peek)
                    k = int(s, 16)
                else:
                    k = 0
                    cond = False
            while cond:
                k = 10 * k + int(self.peek)
                if self.index == len(content) - 1:
                    break
                self.index += 1
                self.error += 1
                self.peek = content[self.index]
                cond = self.peek.isdigit()
            return Token(NUM, k)

        if self.peek.isalpha():
            s = ''
            condition = True
            while condition:
                s += self.peek
                if self.index == len(content) - 1:
                    break
                self.index += 1
                self.error += 1
                self.peek = content[self.index]
                if self.peek.isalpha() or self.peek.isdigit():
                    condition = True
                else:
                    condition = False
            w = self.words.get(s)
            if w is not None:
                return w
            if s == "not":
                return Token(UNAR_NOT)
            elif s == "while":
                return Token(WHILE)
            w = Token(ID, s)
            self.words[s] = w
            return w

        if self.peek == "~":
            self.index += 1
            self.error += 1
            self.peek = content[self.index]
            return Token(INV)

        d = Token(self.peek)
        if self.index < len(content) - 1:
            self.index += 1
            self.error += 1
        self.peek = ' '
        return d
