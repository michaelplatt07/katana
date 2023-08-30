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

; section .text
;     global _start
   
;     _start:
;         ; Set rcx to 0. This will be the bit counter to tell the write how
;         ; many bits to print to the screen.
;         mov rcx, 0
;         ; Put initial values into the registers
;         mov rax, [num]
;         mov rbx, [divisor]
;         mov rdx, 0
;         div rbx
;         add rcx, 8
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
;         add rcx, 8
;         ; If remainder then loop again
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
;         mov rdx, rcx
;         syscall
;         ; mov rsi, rsp
;         ; mov rax, 1
;         ; mov rdi, 1
;         ; mov rdx, 4
;         ; syscall
;         ; pop rax
;         ; mov rsi, rsp
;         ; mov rax, 1
;         ; mov rdi, 1
;         ; mov rdx, 4
;         ; syscall
;         ; pop rax
;         ; mov rsi, rsp
;         ; mov rax, 1
;         ; mov rdi, 1
;         ; mov rdx, 4
;         ; syscall
;         ; pop rax
;         ; mov rsi, rsp
;         ; mov rax, 1
;         ; mov rdi, 1
;         ; mov rdx, 4
;         ; syscall
;         ; pop rax
;         ; mov rsi, rsp
;         ; mov rax, 1
;         ; mov rdi, 1
;         ; mov rdx, 4
;         ; syscall
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
; section .text
;     global _start

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
;     printl_string:
;         ;; Print function
;         ;; Save return address
;         pop rbx
;         ;; Get variable value
;         pop rax
;         ;; Get variable length
;         pop rdx
;         mov rsi, rax
;         mov rax, 1
;         mov rdi, 1
;         syscall
;         ;; Add linefeed.
;         push 10
;         mov rsi, rsp
;         mov rdx, 4
;         mov rax, 1
;         mov rdi, 1
;         syscall
;         ;; Remove value at top of stack.
;         pop rax
;         ;; Add return carriage.
;         push 13
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
;     _start:
;         ;; Get current break address
;         mov rdi, 0
;         mov rax, 12
;         syscall
;         mov rdi, rax

;         ;; Attempt to allocate 6 bytes for string
;         add rdi, 6
;         mov rax, 12
;         syscall

;         ; push rax ; Pushes the address of the memory onto the stack
;         ;; Try declaring a string
;         mov byte [rax], 'H'
;         mov byte [rax+1], 'e'
;         mov byte [rax+2], 'l'
;         mov byte [rax+3], 'l'
;         mov byte [rax+4], 'o'
;         mov byte [rax+5], '!'
;         mov byte [rax+6], 0
;         push 6
;         push rax
;         call printl_string
;         ;; Exit
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Updating a character
; section .text
;     global _start

; section .var_1 write
;     string_1 db 'Hello', 0

; section .text
;     _start:
;         push string_1
;         push 3
;         push 'Q'
;         ; Get the new char 
;         pop rdx
;         ; Get the index to replace
;         pop rbx
;         ; Load up string
;         pop rax
;         ; Move to rdi to replace
;         mov rdi, rax
;         ; Update with the char
;         mov byte [rdi+rbx], dl
;         push 6
;         pop rdx
;         mov rsi, rax
;         mov rax, 1
;         mov rdi, 1
;         syscall
;         ;; Exit
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Different Int Types
; section .text
;     global _start

; section .int_8
;     int_8 db 275

; section .int_16
;     int_16 dw 65535

; section .int_32
;     int_32 dd 4294967295

; section .int_64
;     int_64 dq 4394967295

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


;; Int overflow
; section .text
;     global _start

; section .int_8 write
;     int_8 db 250

; section .int_16 write
;     int_16 dw 65530

; section .int_32 write
;     ; int_32 dd 2147483649
;     int_32 dd 4294967290

; section .text

;     check_int_8_overflow:
;         pop rcx ;; Get return address
;         pop rbx ;; Get current value of variable
;         movzx rbx, al ;; Move 8 bits into the rax registery
;         pop rbx ;; Get value to add
;         add al, bl
;         jnc no_overflow_int_8
;         jc has_overflow_int_8
;         no_overflow_int_8:
;         push rax
;         push rcx
;         ret
;         has_overflow_int_8:
;         mov rax, 60
;         mov rdi, 8
;         syscall

;     check_int_16_overflow:
;         pop rcx ;; Get return address
;         pop rbx ;; Get current value of variable
;         movzx rbx, ax ;; Move 16 bits into the rax registery
;         pop rbx ;; Get value to add
;         add ax, bx
;         jnc no_overflow_int_16
;         jc has_overflow_int_16
;         no_overflow_int_16:
;         push rcx
;         ret
;         has_overflow_int_16:
;         mov rax, 60
;         mov rdi, 16 
;         syscall

;     check_int_32_overflow:
;         pop rcx ;; Get return address
;         pop rax ;; Get current value of variable
;         pop rbx ;; Get value to add
;         add eax, ebx
;         jnc no_overflow_int_32
;         jc has_overflow_int_32
;         no_overflow_int_32:
;         push rcx
;         ret
;         has_overflow_int_32:
;         mov rax, 60
;         mov rdi, 32 
;         syscall

;     _start:
;         ;; Checking int addition overflow for 8 bit number
;         mov al, [int_8]
;         push 1 ;; Won't cause overflow
;         ; push 10  ;; Will cause overflow
;         push rax
;         call check_int_8_overflow
;         pop rax ;; Get the sum back into RAX

;         ;; Checking int addition overflow for 16 bit number
;         mov ax, [int_16]
;         push 1 ;; Won't cause overflow
;         ; push 10  ;; Will cause overflow
;         push rax
;         call check_int_16_overflow

;         ;; Checking int addition overflow for 32 bit number
;         mov eax, [int_32]
;         push 1 ;; Won't cause overflow
;         ; push 10  ;; Will cause overflow
;         push rax
;         call check_int_32_overflow

;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Function declaration and use
; section .text

;     add:
;         pop rcx ;; Get return address
;         pop rbx ;; Get the second parameter of the function
;         pop rax ;; Get the first parameter of the function
;         add rax, rbx ;; Add the numbers
;         push rax ;; Push the sum back onto the stack
;         push rcx ;; Push the return address back on the stack
;         ret ;; Return to main

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
;     global _start

; section .text
;     _start:
;         push 3
;         push 4
;         call add
;         mov rax, 8
;         call print_num ;; This should print the sum

;         ;; Exit
;         mov rax, 60
;         mov rdi, 0
;         syscall


;; Function declaration and use with pointer to args
section .text

    add:
        pop rcx ;; Get return address
        pop rdx ;; Get the pointer to the args
        mov rbx, [rdx] ;; Get the second parameter of the function
        mov rax, [rdx + 8] ;; Get the second parameter of the function
        mov r8, [rdx + 16] ;; Get the pointer to the clean stack
        push 5 ;; Add random to stack to represent doing something
        push 1 ;; Add random to stack to represent doing something
        add rax, rbx ;; Add the numbers
        mov rsp, r8 ;; Reset the pointer to the clean part of the stack
        push rax ;; Push the sum back onto the stack
        push rcx ;; Push the return address back on the stack
        ret ;; Return to main

    print_num:
        ;; Print function
        ;; Save return address
        pop rbx
        ;; Get variable value
        pop rax
        add rax, 48
        push rax
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
    global _start

section .text
    _start:
        push rsp ;; Push the starting point without the args onto the stack
        push 3
        push 4
        push rsp ;; Push pointer to the args on the stack
        call add
        ; mov rax, 8
        call print_num ;; This should print the sum

        ;; Exit
        mov rax, 60
        mov rdi, 0
        syscall
