from Token import Token
from dict import *


class Lexer():
    def __init__(self):
        self.line = 1
        self.index = 0
        self.peek = ' '
        self.words = {}
        self.indent = 0
        self.old_indent = 0
        self.string = False

    def reserve(self, t):
        self.words[t.value] = t

    def scan(self, contents):
        if self.index == len(contents):
            if self.old_indent != 0:
                self.old_indent -= 1
                return Token(DEDENT)
            return Token(ENDMARK)

        self.peek = contents[self.index]

        if self.peek == '"':
            self.string = not self.string
            self.index += 1
            self.peek = contents[self.index]
            return Token(DQM)

        if self.string:
            s = ''
            cond = True
            while cond:
                s += self.peek
                if self.index == len(contents) - 1:
                    break
                self.index += 1
                self.peek = contents[self.index]
                cond = (self.peek != '"')

            w = self.words.get(s)
            if w is not None:
                return w
            w = Token(STRING, s)
            self.words[s] = w
            return w

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

        while (self.index < len(contents) - 1) and not self.string:
            if self.peek == ' ':
                self.index += 1
                self.peek = contents[self.index]
            else:
                break

        if self.peek == "\n":
            self.index += 1
            self.line += 1
            self.indent = 0
            return Token(NL)

        if self.peek.isdigit() and not self.string:
            v = 0
            cond = True
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
