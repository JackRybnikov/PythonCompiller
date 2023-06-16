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
	mov eax, 1
	push eax 
	mov esp, ebp
	pop ebp
      cmp eax, 0
	je _e2
	_e1:
	mov eax, 3
	sub eax, 2
	jmp _post_conditional
	_e2:
	mov eax, 2
	add eax, 10
	_post_conditional:
	invoke MessageBox,0,str$(eax), ADDR Caption, MB_OK
	ret
function endp

start:
	invoke function
	invoke ExitProcess, 0
end start