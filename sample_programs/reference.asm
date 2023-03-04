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


; ; Strings
; section .text
;     global _start

; section .something_1
;     msg db  'Hello, world!', 10 ;our dear string
;     len equ $ - msg         ;length of our dear string

; section .text
;     _start:
;         mov rsi, msg
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, len
;         syscall

;         mov rax, 60
;         mov rdi, 0
;         syscall


; Function params
; section .text
;     global _start

; section .string_1
;     string_1 db  'Hello, world!', 10 ;our dear string
;     len_1 equ $ - string_1         ;length of our dear string

; section .text

;     print:
;         pop rbx
;         pop rax
;         mov rsi, rax
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, len_1
;         syscall
;         push rbx
;         ret
 
;     _start:
;         push string_1
;         call print
;         mov rax, 60
;         mov rdi, 0
;         syscall


; Printing a variable
; section .text
;     global _start

; section .var_1
;     number_1 dw 4

; section .text
;     _start:
;         mov rax, [number_1]
;         add rax, 48
;         push rax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         syscall

;         mov rax, 60
;         mov rdi, 0
;         syscall


; Booleans
; section .text
;     global _start

; section .var_1
;     bool_1 db 0

; section .text
;     _start:
;         mov rax, [bool_1]
;         cmp rax, 0
;         je equal
;         jne not_equal
;         equal:
;         mov rax, 49
;         push rax
;         jmp end_cond
;         not_equal:
;         mov rax, 50
;         push rax
;         end_cond:
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 4
;         syscall
;         syscall

;         mov rax, 60
;         mov rdi, 0
;         syscall


; Working with chars
; section .text
;     global _start
; section .string_1
;     char_1 db 'j'
; section .text
;     _start:
;         mov rsi, char_1
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall
;         mov rax, 60
;         mov rdi, 0
;         syscall


; String indices
; section .text
;     global _start

; section .string_1
;     string_1 db 'hELLO'
;     char_1 db 'h'

; ;; This will get the single byte from string_1 and put it in al, the lower 8
; ;; bytes of register ax (16 bits).
; section .text
;     _start:
;         ;; H
;         mov al, [string_1]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall
        
;         ;; Compare a byte to a byte.
;         mov al, [string_1]
;         cmp al, [char_1]
;         jne not_rest
;         je rest
;         not_rest:
;         mov al, [string_1 + 1]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall
;         rest:
;         ;; e
;         mov al, [string_1 + 1]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; l
;         mov al, [string_1 + 2]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; l
;         mov al, [string_1 + 3]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         ;; 0
;         mov al, [string_1 + 4]
;         push ax
;         mov rsi, rsp
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, 1
;         syscall

;         mov rax, 60
;         mov rdi, 0
;         syscall

;; Appending string
; section .text
;     global _start

; section .string_1 write
;     string_1 db 'Hello', 5
;     len equ $ - string_1

; section .text
;     _start:
;         mov al, '!'
;         mov byte [string_1+5], al
;         mov rsi, string_1
;         mov rax, 1
;         mov rdi, 1
;         mov rdx, len
;         syscall
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Calculate string length
; section .text
;     global _start

; section .string_1 write
;     string_1 db 'Hello'

; section .text
;     print_num:
;         ;; Print function
;         ;; Save return address
;         pop rbx
;         ;; Get variable value
;         pop rax
;         add rax, 48
;         push rax
;         mov rsi, rsp
;         mov rdx, 4
;         mov rax, 1
;         mov rdi, 1
;         syscall
;         ;; Remove value at top of stack.
;         pop rax
;         ;; Push return address back.
;         push rbx
;         ret

; section .text
;     string_length:
;         ;; Save return address
;         pop rbx
;         ;; Get string to loop over
;         pop rax
;         pop rcx
;         loop_str_len:
;             cmp byte[rax], 0
;             jne loop_again
;             je end
;         loop_again:
;             inc rax
;             jmp loop_str_len
;         end:
;             ;; Calculate actual difference in length
;             sub rax, rcx
;             push rax
;             ;; Push return address onto stack
;             push rbx
;             ret

; section .text
;     _start:
;         push string_1
;         push string_1
;         call string_length
;         call print_num
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Dynamic heap allocation.
section .text
    global _start

section .text
    string_length:
        ;; Save return address
        pop rbx
        ;; Get string to loop over
        pop rax
        pop rcx
        loop_str_len:
            cmp byte[rax], 0
            jne loop_again
            je end
        loop_again:
            inc rax
            jmp loop_str_len
        end:
            ;; Calculate actual difference in length
            sub rax, rcx
            push rax
            ;; Push return address onto stack
            push rbx
            ret

section .text
    printl_string:
        ;; Print function
        ;; Save return address
        pop rbx
        ;; Get variable value
        pop rax
        ;; Get variable length
        pop rdx
        mov rsi, rax
        mov rax, 1
        mov rdi, 1
        syscall
        ;; Add linefeed.
        push 10
        mov rsi, rsp
        mov rdx, 4
        mov rax, 1
        mov rdi, 1
        syscall
        ;; Remove value at top of stack.
        pop rax
        ;; Add return carriage.
        push 13
        mov rsi, rsp
        mov rdx, 4
        mov rax, 1
        mov rdi, 1
        syscall
        ;; Remove value at top of stack.
        pop rax
        ;; Push return address back.
        push rbx
        ret

section .text
    _start:
        ;; Get current break address
        mov rdi, 0
        mov rax, 12
        syscall
        mov rdi, rax

        ;; Attempt to allocate 6 bytes for string
        add rdi, 6
        mov rax, 12
        syscall

        ; push rax ; Pushes the address of the memory onto the stack
        ;; Try declaring a string
        mov byte [rax], 'H'
        mov byte [rax+1], 'e'
        mov byte [rax+2], 'l'
        mov byte [rax+3], 'l'
        mov byte [rax+4], 'o'
        mov byte [rax+5], '!'
        mov byte [rax+6], 0
        push 6
        push rax
        call printl_string
        ;; Exit
        mov rax, 60
        mov rdi, 0
        syscall
