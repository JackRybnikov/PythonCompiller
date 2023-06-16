from Parser import start

a = f".386\n" \
    f".model flat, stdcall\n\n" \
    f"option casemap: none;\n" \
    f"include C:\masm32\include\kernel32.inc\n"\
    "include C:\masm32\include\windows.inc\n"\
    "include C:\masm32\include\masm32rt.inc\n"\
    "include C:\masm32\include\\user32.inc\n" \
    "includelib C:\masm32\lib\kernel32.lib\n" \
    "includelib C:\masm32\lib\\user32.lib\n" \
    ".data\n" \
    "Caption db 'Rybnikov', 0\n" \
    ".code\n\n"

a = start(a)
b = open("3-20-Python-IO-81-Rybnikov.asm", "w")
b.write(a)
b.close()