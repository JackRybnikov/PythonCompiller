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
        self.value = {}
        self.tokens = []
        self.indent = 0
        self.old_indent = 0
        self.spaces = 0

    def reserve(self, t):
        self.words[t.value] = t

    def goError(self):
        return self.line

    def scan(self, contents):
        if self.index == len(contents):
            if self.old_indent != 0:
                self.old_indent -= 1
                self.tokens.append(DEDENT)
                return Token(DEDENT)
            self.tokens.append(ENDMARK)
            return Token(ENDMARK)

        self.peek = contents[self.index]

        while self.peek == '\t':
            self.indent += 1
            self.index += 1
            self.peek = contents[self.index]

        while self.index < len(contents) - 1:
            if self.peek == ' ':
                self.index += 1
                self.spaces += 1
                self.peek = contents[self.index]
            else:
                self.indent += self.spaces // 4
                self.spaces = 0
                break

        if self.old_indent < self.indent:
            self.old_indent += 1
            self.tokens.append(INDENT)
            return Token(INDENT)
        elif self.old_indent > self.indent:
            self.old_indent -= 1
            self.tokens.append(DEDENT)
            return Token(DEDENT)

        if self.peek == "'" or self.peek == '"':
            # print("Нашли кавычки")
            s = ''
            cond = True
            while cond:
                s += self.peek
                self.index += 1
                self.peek = contents[self.index]
                cond = (self.peek != '"' and self.peek != "'")
                if self.index == len(contents) - 1:
                    break
            s += self.peek
            self.index += 1
            self.peek = contents[self.index]
            self.tokens.append(STRING)
            return Token(STRING, s)

        if self.peek == "\n":
            self.index += 1
            self.line += 1
            self.indent = 0
            return Token(NL)

        if self.peek.isdigit():
            v = 0
            cond = True
            if self.peek == '0':
                self.index += 1
                self.peek = contents[self.index]
                if self.peek == 'x':
                    s = ''
                    self.index += 1
                    self.peek = contents[self.index]
                    while cond:
                        s += self.peek
                        if self.index == len(contents) - 1:
                            break
                        self.index += 1
                        self.peek = contents[self.index]
                        cond = is_hex(self.peek)
                    v = int(s, 16)
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
            if s == "not":
                return Token(UNAR_NOT)
            w = Token(ID, s)
            self.words[s] = w
            return w

        t = Token(self.peek)
        if self.index < len(contents) - 1:
            self.index += 1
        self.peek = ' '
        return t
