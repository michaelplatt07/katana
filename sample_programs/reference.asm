; Example of a simple add
;section .text
;    global _start
;
;    _start:
;        mov rax, 2
;        mov rbx, 3
;        add rax, rbx
;        add rax, 48
;        push rax
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        mov rax, 60
;        mov rdi, 0
;        syscall


; Example of a simple multiply
; section .text
;     global _start
;
;     _start:
;         mov rax, 2
;         mov rbx, 3
;         mul rbx
;         add rax, 48
;         push rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         mov rax, 60
;         mov rdi, 0
;         syscall


; Loops
;section .text
;    global _start
;
;    _start:
;        ; Move a value to rcx to loop
;        mov rcx, 10
;        ; Loop 10 times
;        l1:
;            mov rbx, rcx
;            push 48
;            mov rsi, rsp
;            mov rax, 1
;            mov rdi, 1
;            mov rdx, 4
;            syscall
;            mov rcx, rbx
;            loop l1
;        mov rax, 60
;        mov rdi, 0
;        syscall


; Simple conditional
;section .data
;    num db 12
;
;section .text
;    global _start
;
;    _start:
;        mov rax, [num]
;        mov rbx, 12
;        cmp rbx, rax
;        je equal
;        jne notequal
;    equal:
;        ; Going to return 1
;        push 49
;        ; Print
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        ; Exit
;        mov rax, 60
;        mov rdi, 0
;        syscall
;        ret
;    notequal:
;        ; Going to return 0
;        push 48
;        ; Print
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        ; Exit
;        mov rax, 60
;        mov rdi, 0
;        syscall
;        ret


; Simple divide
;section .data
;    num dw 12
;
;section .text
;    global _start
;
;    _start:
;        mov rax, [num]
;        mov rbx, 10
;        div rbx
;        mov rbx, rdx
;        ; Push the quotient onto the stack
;        add rax, 48
;        push rax
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        ; Push the remainder onto the stack
;        add rbx, 48
;        push rbx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        mov rax, 60
;        mov rdi, 0
;        syscall


; Print a number
;section .data
;    num dq 12345
;    divisor dq 10
;
;section .text
;    global _start
;
;    _start:
;        ; Put initial number into register
;        mov rax, [num]
;
;        ; Print first number
;        mov rbx, [divisor]
;        mov rdx, 0
;        div rbx
;        ; Move rax (quotient) into rbx to reuse
;        mov rbx, rax
;        ; Push the remainder onto the stack
;        add rdx, 48
;        push rdx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;
;        ; Print second number
;        mov rax, rbx
;        mov rbx, [divisor]
;        mov rdx, 0
;        div rbx
;        ; Move rax (quotient) into rbx to reuse
;        mov rbx, rax
;        ; Push the remainder onto the stack
;        add rdx, 48
;        push rdx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;
;        ; Print third number
;        mov rax, rbx
;        mov rbx, [divisor]
;        mov rdx, 0
;        div rbx
;        ; Move rax (quotient) into rbx to reuse
;        mov rbx, rax
;        ; Push the remainder onto the stack
;        add rdx, 48
;        push rdx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;
;        ; Print fourth number
;        mov rax, rbx
;        mov rbx, [divisor]
;        mov rdx, 0
;        div rbx
;        ; Move rax (quotient) into rbx to reuse
;        mov rbx, rax
;        ; Push the remainder onto the stack
;        add rdx, 48
;        push rdx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;
;        ; Print fifth number
;        mov rax, rbx
;        mov rbx, [divisor]
;        mov rdx, 0
;        div rbx
;        ; Move rax (quotient) into rbx to reuse
;        mov rbx, rax
;        ; Push the remainder onto the stack
;        add rdx, 48
;        push rdx
;        ; Print value
;        mov rsi, rsp
;        mov rax, 1
;        mov rdi, 1
;        mov rdx, 4
;        syscall
;        mov rax, 60
;        mov rdi, 0
;        syscall


; Print a number with loop
; section .data
;     num dq 12345
;     divisor dq 10
;
; section .text
;     global _start
;    
;     _start:
;         ; Put initial values into the registers
;         mov rax, [num]
;         mov rbx, [divisor]
;         mov rdx, 0
;         div rbx
;         ; Move rax (quotient) into rbx to reuse
;         mov rbx, rax
;         ; Push the remainder onto the stack
;         add rdx, 48
;         push rdx
;     l1:
;         mov rax, rbx 
;         mov rbx, [divisor]
;         mov rdx, 0
;         div rbx
;         ; Move rax (quotient) into rbx to reuse
;         mov rbx, rax
;         ; Push the remainder onto the stack
;         add rdx, 48
;         push rdx
;         ; Print value
;         cmp rbx, 0
;         ; If no numbers remain
;         je exit
;         ; If numbers left continue to loop
;         jne l1
;     exit:
;         ; Print value
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         pop rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         pop rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         pop rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         pop rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Print command line arg count, program name, and all command
;; line args. Must be run as ./reference arg1 arg2 arg3 arg4
; section .text
;     global _start
;     _start:
;         ;; Pop argc
;         pop rbx 
;         add rbx, 48
;         push rbx
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall

;         ;; Pop function name
;         pop rbx
;         mov rsi, [rsp]
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 5
;         syscall

;         ;; Pop arg 1
;         pop rbx
;         mov rsi, [rsp]
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; Pop arg 2
;         pop rbx
;         mov rsi, [rsp]
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; Pop arg 3
;         pop rbx
;         mov rsi, [rsp]
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; Pop arg 4
;         pop rbx
;         mov rsi, [rsp]
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; Exit
;         mov rax, 60
;         mov rdi, 0
;         syscall


; Example of function calls
; section .text

;     print:
;         add rax, 48
;         push rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         pop rax
;         ret
 
;     global _start

;     _start:
;         mov rax, 2
;         mov rbx, 3
;         add rax, rbx
;         call print
;         mov rax, 60
;         mov rdi, 0
;         syscall


; While loops
; section .text
;     global _start

;     _start:
;         ;; Initialize the registry
;         mov rcx, 0
;         loop:
;             mov rbx, rcx
;             push 49
;             mov rsi, rsp
;             mov rax, 1
;             mov rdi, 1
;             mov rdx, 4
;             syscall
;             mov rcx, rbx
;             inc rcx
;             cmp rcx, 5
;             jl loop

;         mov rax, 60
;         mov rdi, 0
;         syscall

