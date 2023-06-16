import os
from Parser import start

a = f".386\n" \
    f".model flat, stdcall\n\n" \
    f"option casemap: none;\n" \
    f"include E:\masm32\include\kernel32.inc\n" \
    f"include E:\masm32\include\windows.inc\n" \
    f"include E:\masm32\include\masm32rt.inc\n" \
    f"include E:\masm32\include\\user32.inc\n" \
    f"includelib E:\masm32\lib\kernel32.lib\n" \
    f"includelib E:\masm32\lib\\user32.lib\n" \
    f".data\n" \
    f"Caption db 'Rybnikov', 0\n" \
    f".code\n\n"

a = start(a)
b = open("6-20-Python-IO-81-Rybnikov.asm", "w")
b.write(a)
b.close()
c = open("6-20-Python-IO-81-Rybnikov.asm", "r")
line = c.readline()
while line:
    print(line)
    line = c.readline()
c.close()
os.system("PAUSE")
