from Parser import program

s = ".386\n.model flat, stdcall\n" + \
    "option casemap: none;\n" +\
    "include E:\\\\masm32\include\windows.inc\n" +\
    "include E:\\\\masm32\include\kernel32.inc\n" +\
    "include E:" + "\\\\" + "masm32" + "\\" + "include" + "\\" + "user32.inc\n" +\
    "include E:\\\\masm32\include\masm32rt.inc\n" +\
    "\n" +\
    "includelib E:" + "\\\\" + "masm32" + "\\" + "lib" + "\\" + "user32.lib\n" +\
    "includelib E:\\\\masm32\lib\kernel32.lib\n\n"+\
    ".data\n.code\n"
s = program(s)
a = open("1-20-Python-IO-81-Rybnikov.asm", "w")
a.write(s)
a.close()
