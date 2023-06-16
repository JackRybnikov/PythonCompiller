.386
.model flat, stdcall

option casemap: none;
include E:\masm32\include\kernel32.inc
include E:\masm32\include\windows.inc
include E:\masm32\include\masm32rt.inc
include E:\masm32\include\user32.inc
includelib E:\masm32\lib\kernel32.lib
includelib E:\masm32\lib\user32.lib
.data
Caption db 'Rybnikov', 0
.code


function proc
	mov eax, 1
	mov ebx, 0
	mov ecx, 1
	mov edx, 30

	cycle:
	sub edx, 1
	add ecx, ebx
	mov ebx, eax
	mov eax, ecx
	cmp edx, 2
	jne cycle

	fn MessageBox,0,str$(ecx),"Rybnikov",MB_OK
	ret
function endp
start:
	invoke function
	invoke ExitProcess, 0
end start