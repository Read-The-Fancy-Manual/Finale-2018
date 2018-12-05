section .data
  pwd db "-.-.-.-.-.-.-.-.-.-.-."
  key db 0x84,0x78,0x82,0x80,0x74,0x85,0x99,0x93,0x81,0x69,0x69,0x84,0x7a,0x70,0x84,0x7a,0x7a,0x80,0x65,0x79,0x9e,0x00
  banner db "RTFM little crackme :)",10,"Password : "
  wrong db "Nope :(",10
  right db "Well played :)", 10
section .text
  global _start
_start:
  xor rbx, rbx
display_banner:	
  mov rdx, 34
  mov rsi, dword banner
  mov rax, 1
  mov rdi, 1
  syscall
read_entry:	
  mov rdx, 22
  mov rsi, dword pwd
  mov rax, 0
  mov rdi, 0
  syscall

check:
  xor rbx, rbx
  xor rdx, rdx
  xor rcx, rcx
  mov bl, [rsi]
  mov rdi, dword key
  add rsi, 1
loop:
  cmp rdx, 21
  je win
  mov al, bl
  mov bl, [rsi]
  add rax, rbx
  sub rax, 88
  mov cl, [rdi]	
  add rsi, 1
  add rdi, 1
  add rdx, 1
  cmp rax, rcx
  je loop
fail:	
  mov rdx, 8
  mov rsi, dword wrong
  mov rax, 1
  mov rdi, 1
  syscall
  jmp short exit
win:
  sub rsi, 1
  mov bl, [rsi]
  cmp bl, 0x7d
  jne fail	
  mov rdx, 15
  mov rsi, dword right
  mov rax, 1
  mov rdi, 1
  syscall
exit:
  mov rax, 0x3c
  syscall	
