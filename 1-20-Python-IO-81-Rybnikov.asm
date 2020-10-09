.386
.model flat, stdcall
option casemap: none;
include E:\\masm32\include\windows.inc
include E:\\masm32\include\kernel32.inc
include E:\\masm32\include\user32.inc
include E:\\masm32\include\masm32rt.inc

includelib E:\\masm32\lib\user32.lib
includelib E:\\masm32\lib\kernel32.lib

.data
.code

alfa PROC
	mov eax, 43981
	fn MessageBox,0,str$(eax),"Rybnikov",MB_OK
	ret
alfa ENDP

main PROC
	mov eax, 123
	fn MessageBox,0,str$(eax),"Rybnikov",MB_OK
	ret
main ENDP

maina PROC
	mov ecx, 7
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	mov eax, ecx
	fn MessageBox,0,str$(eax),"Rybnikov",MB_OK
	ret
maina ENDP

mainb PROC
	mov ecx, 7
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	mov eax, ecx
	fn MessageBox,0,str$(eax),"Rybnikov",MB_OK
	ret
mainb ENDP

start:
	invoke main
	invoke alfa
	mov ecx, 5
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	cmp ecx, 0
	pushf
	xor ecx, ecx
	popf
	setz cl
	mov eax, ecx
	add eax, 10
	add eax, 20
	add eax, 30
	invoke maina
	invoke mainb
	invoke ExitProcess, 0
end start