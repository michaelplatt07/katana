import pytest
import os
from katana.katana import (
    Compiler,
    Lexer,
    Parser,
    Program
)


def get_compiler_class(lines):
    program = Program(lines)
    lexer = Lexer(program)
    token_list = lexer.lex()
    parser = Parser(token_list)
    ast = parser.parse()
    return Compiler(ast)


def get_assembly_for_program(lines):
    compiler = get_compiler_class(lines)
    return compiler.get_assembly()


class TestComiplerSingleNodes:

    def test_literal_nubmer(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_literal.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 3\n",
            ]


class TestCompilerMathematics:

    def test_simple_add(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_add.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
            ]

    def test_simple_sub(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_sub.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Subtract\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    sub rbx, rax\n",
                "    push rbx\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Subtract\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    sub rbx, rax\n",
                "    push rbx\n",
            ]

    def test_simple_multiply(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_multiply.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
            ]

    def test_simple_divide(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_divide.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Divide\n",
                "    pop rbx\n",
                "    pop rax\n",
                "    div rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Divide\n",
                "    pop rbx\n",
                "    pop rax\n",
                "    div rbx\n",
                "    push rax\n",
            ]

    def test_complicated_mathematics(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_mathematics.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Push number onto stack\n",
                "    push 4\n",
                "    ;; Divide\n",
                "    pop rbx\n",
                "    pop rax\n",
                "    div rbx\n",
                "    push rax\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
            ]


class TestCompilerParenthesis:

    def test_add_higher_prio_than_mult_with_paren(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_parenthesis.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
            ]


class TestCompilerKeywords:

    def test_print_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_print.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Keyword Func\n",
                "    call print_num\n",
            ]

    def test_printl_keyword_with_num(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_printl.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Keyword Func\n",
                "    call printl_num\n",
            ]

    def test_printl_keyword_with_char(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_printl_char.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Keyword Func\n",
                "    call printl_char\n",
                "    ;; Pop the byte off the stack to clean up\n",
                "    pop bx\n",
            ]

    def test_printl_keyword_with_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_printl_string.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
            ]

    def test_main_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_main.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 14\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
            ]

    def test_assignment_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 3\n"
                    ]
                }
            }
            assert assembly == [
            ]

    @pytest.mark.skip
    def test_assign_new_value_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assign_new_value_to_string.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 5,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 db 'Hello'\n",
                        "    len_1 equ $ - 5\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_assign_new_value_char(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assign_new_value_to_char.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "char_1",
                    "var_type": "char",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    char_1 db 'a'\n"
                    ]
                }
            }
            assert assembly == [
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Assign new value to char var\n",
                "    mov rdi, char_1\n",
                "    mov byte [rdi], bl\n",
                "    pop bx\n",
                "    ;; Push char var onto stack\n",
                "    mov bl, [char_1]\n",
                "    push bx\n",
                "    ;; Keyword Func\n",
                "    call print_char\n",
                "    ;; Pop the byte off the stack to clean up\n",
                "    pop bx\n",
            ]

    def test_assign_new_value_int(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assign_new_value_to_int.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 0\n"
                    ]
                }
            }
            assert assembly == [
                "    ;; Assign new int to int var\n",
                "    mov word [number_1], 1\n",
                "    ;; Push var val onto stack\n",
                "    push qword [number_1]\n",
                "    ;; Keyword Func\n",
                "    call print_num\n"
            ]

    def test_assignment_keyword_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assignment_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 3\n"
                    ]
                }
            }
            assert assembly == [
                "    ;; Push var val onto stack\n",
                "    push qword [number_1]\n",
                "    ;; Keyword Func\n",
                "    call print_num\n"
            ]

    def test_string_keyword_assignment(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 5,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 db 'hello'\n",
                        "    len_1 equ $ - 5\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_char_keyword_assignment(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_char_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "char_1",
                    "var_type": "char",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    char_1 db 'h'\n",
                    ]
                }
            }
            assert assembly == [
            ]

    def test_raw_char_keyword_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_raw_char_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
            }
            assert assembly == [
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Keyword Func\n",
                "    call print_char\n",
                "    ;; Pop the byte off the stack to clean up\n",
                "    pop bx\n",
            ]

    def test_char_keyword_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_char_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "char_1",
                    "var_type": "char",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    char_1 db 'A'\n",
                    ]
                }
            }
            assert assembly == [
                "    ;; Push char var onto stack\n",
                "    mov bl, [char_1]\n",
                "    push bx\n",
                "    ;; Keyword Func\n",
                "    call print_char\n",
                "    ;; Pop the byte off the stack to clean up\n",
                "    pop bx\n",
            ]

    def test_char_compare(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_char_compare.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push char var onto stack\n",
                "    mov bl, [char_1]\n",
                "    push bx\n",
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Pop values for comparing equal on char\n",
                "    pop ax\n",
                "    pop bx\n",
                "    cmp bx, ax\n",
                "    je equal_1\n",
                "    jne not_equal_1\n",
                "    equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    not_equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; End if/else block\n",
                "    end_1:\n"
            ]

    def test_set_char_var_to_char_at(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_char_at_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 14\n",
                "    push raw_string_1\n",
                "    ;; Push number onto stack\n",
                "    push 2\n",
                "    ;; Keyword Func\n",
                "    call char_at\n",
                "    ;; Pop return value of char at\n",
                "    pop ax\n",
                "    ;; Update var with value\n",
                "    mov rdi, char_1\n",
                "    mov byte [rdi], al\n",
                "    ;; Push char var onto stack\n",
                "    mov bl, [char_1]\n",
                "    push bx\n",
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Pop values for comparing equal on char\n",
                "    pop ax\n",
                "    pop bx\n",
                "    cmp bx, ax\n",
                "    je equal_1\n",
                "    jne not_equal_1\n",
                "    equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    not_equal_1:\n",
                "    ;; End if/else block\n",
                "    end_1:\n",
            ]

    def test_set_var_to_another_var(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_set_var_to_another.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    push qword [number_2]\n",
                "    pop rax\n",
                "    ;; Assign var value to new var\n",
                "    mov qword [number_1], rax\n"
            ]

    def test_bool_false_keyword_assignment(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_bool_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "bool_1",
                    "var_type": "bool",
                    "var_len": 5,
                    "asm": [
                        "section .var_1 write\n",
                        "    bool_1 dq 0\n",
                    ]
                }
            }
            assert assembly == [
            ]

    def test_bool_true_keyword_assignment(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_bool_true_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "bool_1",
                    "var_type": "bool",
                    "var_len": 4,
                    "asm": [
                        "section .var_1 write\n",
                        "    bool_1 dq 1\n",
                    ]
                }
            }
            assert assembly == [
            ]

    def test_bool_keyword_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_bool_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "bool_1",
                    "var_type": "bool",
                    "var_len": 4,
                    "asm": [
                        "section .var_1 write\n",
                        "    bool_1 dq 1\n",
                    ]
                }
            }
            assert assembly == [
                "    ;; Push var val onto stack\n",
                "    push qword [bool_1]\n",
                "    ;; Push true onto stack\n",
                "    push 1\n",
                "    ;; Pop values for comparing equal on other\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    cmp rbx, rax\n",
                "    je equal_1\n",
                "    jne not_equal_1\n",
                "    equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 4\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    not_equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; End if/else block\n",
                "    end_1:\n",
            ]

    def test_if_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_conditional_if_only.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Pop values for comparing greater than\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    cmp rbx, rax\n",
                "    jg greater_1\n",
                "    jle less_1\n",
                "    greater_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    less_1:\n",
                "    ;; End if/else block\n",
                "    end_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n"
            ]

    def test_if_else_keyword_with_less_than(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_conditional_if_else_less_than.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Pop values for comparing less than\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    cmp rbx, rax\n",
                "    jl less_1\n",
                "    jge greater_1\n",
                "    less_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 10\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    greater_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 13\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; End if/else block\n",
                "    end_1:\n"
            ]

    def test_if_else_keyword_with_equal(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_conditional_if_else_equal.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 1\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Pop values for comparing equal on other\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    cmp rbx, rax\n",
                "    je equal_1\n",
                "    jne not_equal_1\n",
                "    equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 5\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    jmp end_1\n",
                "    not_equal_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; End if/else block\n",
                "    end_1:\n"
            ]

    def test_loop_up(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    push 0\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Loop up\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    pop rbx\n",
                "    pop rcx\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    push rcx\n",
                "    push rbx\n",
                "    jl loop_1\n",
                "    ;; Clean up loop vars\n",
                "    pop rax\n",
                "    pop rax\n"
            ]

    def test_loop_down(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_down.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    push 0\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Loop down\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    pop rcx\n",
                "    pop rbx\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    push rbx\n",
                "    push rcx\n",
                "    jg loop_1\n",
                "    ;; Clean up loop vars\n",
                "    pop rax\n",
                "    pop rax\n"
            ]

    def test_loop_from_ascending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_ascending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Loop up\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    pop rbx\n",
                "    pop rcx\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    push rcx\n",
                "    push rbx\n",
                "    jl loop_1\n",
                "    ;; Clean up loop vars\n",
                "    pop rax\n",
                "    pop rax\n"
            ]

    def test_loop_from_descending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_descending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Loop down\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    pop rbx\n",
                "    pop rcx\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    push rcx\n",
                "    push rbx\n",
                "    jg loop_1\n",
                "    ;; Clean up loop vars\n",
                "    pop rax\n",
                "    pop rax\n"
            ]


class TestCompilerString:

    def test_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 13\n",
                "    push raw_string_1\n",
            ]

    def test_concatenate_char_to_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string_concatenation.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 6,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 db 'Hello'\n",
                        "    len_1 equ $ - 5\n"
                    ]
                }
            }
            assert assembly == [
                "    ;; Push string length and val onto stack\n",
                "    push 5\n",
                "    push string_1\n",
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Concat string\n",
                "    pop ax\n",
                "    pop rbx\n",
                "    ;; Remove string length from stack\n",
                "    pop rcx\n",
                "    ;; Append char to string\n",
                "    mov byte [rbx+5], al\n",
                "    ;; Push string length and val onto stack\n",
                "    push 6\n",
                "    push string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
            ]


class TestCompilerMultipleVarDeclarations:

    def test_multiple_var_type_declarations(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_multi_var_type_declaration.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.compile()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "var_len": 1,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 1\n",
                    ]
                },
                "y": {
                    "section": "var_2",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 14,
                    "asm": [
                        "section .var_2 write\n",
                        "    string_1 db 'Hello, Katana!'\n",
                        "    len_1 equ $ - 14\n"
                    ]
                },
                "z": {
                    "section": "var_3",
                    "var_name": "char_1",
                    "var_type": "char",
                    "var_len": 1,
                    "asm": [
                        "section .var_3 write\n",
                        "    char_1 db 'A'\n",
                    ]
                }
            }
