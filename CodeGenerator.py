from Parser import program

s = ".386\n.model flat, stdcall\n.data\n.code\n"
s = program(s)
a = open("1-20-Python-IO-81-Rybnikov.asm", "w")
a.write(s)
a.close()
