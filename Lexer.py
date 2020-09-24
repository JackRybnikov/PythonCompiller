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
        self.peek = ' '
        self.words = {}
        self.indent = 0
        self.old_indent = 0

    def reserve(self, t):
        self.words[t.value] = t

    def scan(self, contents):
        if self.index == len(contents):
            if self.old_indent != 0:
                self.old_indent -= 1
                return Token(DEDENT)
            return Token(ENDMARK)

        self.peek = contents[self.index]

        while self.peek == '\t':
            self.indent += 1
            self.index += 1
            self.peek = contents[self.index]

        if self.old_indent < self.indent:
            self.old_indent += 1
            return Token(INDENT)
        elif self.old_indent > self.indent:
            self.old_indent -= 1
            return Token(DEDENT)

        while self.index < len(contents) - 1:
            if self.peek == ' ':
                self.index += 1
                self.peek = contents[self.index]
            else:
                break

        if self.peek == '"':
            print("Нашли кавычки")
            s = ''
            cond = True
            while cond:
                s += self.peek
                self.index += 1
                self.peek = contents[self.index]
                cond = (self.peek != '"')
                if self.index == len(contents) - 1:
                    break
            s += self.peek
            self.index += 1
            self.peek = contents[self.index]
            return Token(STRING, s)

        if self.peek == "\n":
            self.index += 1
            self.line += 1
            self.indent = 0
            return Token(NL)

        if self.peek.isdigit():
            cond = True
            condition = True
            v = int(self.peek)
            if self.index == len(contents) - 1:
                condition = False
            if condition:
                self.index += 1
                self.peek = contents[self.index]
                cond = self.peek.isdigit()
            if self.peek == "x" and v == 0:
                v = ''
                while cond:
                    v += self.peek
                    if self.index == len(contents) - 1:
                        break
                    self.index += 1
                    self.peek = contents[self.index]
                    cond = is_hex(self.peek)
                v = int(v, 16)
            else:
                while cond:
                    v = 10 * v + int(self.peek)
                    if self.index == len(contents) - 1:
                        break
                    self.index += 1
                    self.peek = contents[self.index]
                    cond = self.peek.isdigit()
            return Token(NUM, v)

        if self.peek.isalpha():
            s = ''
            cond = True
            while cond:
                s += self.peek
                if self.index == len(contents) - 1:
                    break
                self.index += 1
                self.peek = contents[self.index]
                cond = self.peek.isalpha()
            w = self.words.get(s)
            if w is not None:
                return w
            w = Token(ID, s)
            self.words[s] = w
            return w

        t = Token(self.peek)
        if self.index < len(contents) - 1:
            self.index += 1
        self.peek = ' '
        return t
