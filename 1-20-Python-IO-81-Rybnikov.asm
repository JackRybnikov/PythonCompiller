.386
.model flat, stdcall
.data
.code

alfa PROC
	mov eax, 123
	ret
alfa ENDP

main PROC
	mov eax, 321
	ret
main ENDP

_start:
	invoke main
	invoke alfa
	invoke ExitProcess, 0