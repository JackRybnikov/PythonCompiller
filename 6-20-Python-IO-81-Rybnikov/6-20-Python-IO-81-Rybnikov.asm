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
	push ebp
	mov ebp, esp
	mov eax, 3
	push eax 
	mov esp, ebp
	pop ebp
	cmp eax, -3
	cycle:
	sub eax, 7
	cmp eax, ecx
	jne cycle
	invoke MessageBox,0,str$(eax), ADDR Caption, MB_OK
	ret
function endp

start:
	invoke function
	invoke ExitProcess, 0
end start