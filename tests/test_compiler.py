import pytest
import os
from katana.katana import (
    Compiler,
    Lexer,
    Parser,
    Program,
)


def get_token_list(lines):
    program = Program(lines)
    lexer = Lexer(program)
    return lexer.lex()


def get_nodes(token_list):
    parser = Parser(token_list)
    parser.parse()
    return parser.get_nodes()


def get_compiler_class(lines=None, input_nodes=None):
    if not input_nodes:
        token_list = get_token_list(lines)
        nodes = get_nodes(token_list)
    else:
        nodes = input_nodes
    return Compiler(nodes)


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
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
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
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
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
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
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


class TestCompilerPrint:
    """
    All tests related to the print keyword.
    """
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

    def test_printl_keyword_with_addition(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_printl_addition.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push number onto stack\n",
                "    push 5\n",
                "    ;; Push number onto stack\n",
                "    push 4\n",
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call printl_num\n",
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
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": "3",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
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


class TestCompilerMain:
    """
    All tests related to the main keyword. 
    """

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


class TestCompilerInt:
    """
    All tests related to the int keyword
    """

    def test_declare_int_const(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": "3",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 dq 3\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_declare_int_8_const(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_int_8.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "int_type": "int8",
                    "var_type": "num",
                    "var_len": 1,
                    "var_val": "3",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 db 3\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_declare_int_16_const(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_int_16.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "int_type": "int16",
                    "var_len": 5,
                    "var_val": "62535",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 dw 62535\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_declare_int_32_const(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_int_32.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "int_type": "int32",
                    "var_len": 10,
                    "var_val": "4214967295",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 dd 4214967295\n"
                    ]
                }
            }
            assert assembly == [
            ]

    def test_const_int_being_declared(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_const_int.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "int_type": "int64",
                    "var_type": "num",
                    "var_len": 1,
                    "var_val": "0",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 dq 0\n"
                    ]
                }
            }

    def test_int_declared_from_expression_addition(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_int_from_expression_addition.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": 7,
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 7\n"
                    ]
                }
            }

    def test_int_declared_from_expression_subtraction(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_int_from_expression_subtraction.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "number_1",
                    "var_type": "num",
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": 2,
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    number_1 dq 2\n"
                    ]
                }
            }

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
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": "0",
                    "is_const": False,
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


class TestCompilerString:
    """
    All tests related to the string keyword.
    """

    def test_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 13\n",
                "    push raw_string_1\n",
            ]

    def test_string_with_const_keyword_assignment(self):
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
                    "var_val": "hello",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    string_1 db 'hello', 0\n",
                    ]
                }
            }
            assert assembly == [
            ]

    def test_non_const_string_keyword_assignment(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string_not_const.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 14,
                    "var_val": "Hello, Katana!",
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 dq 0\n",
                    ]
                }
            }
            assert compiler.initialize_vars_asm == [
                "    push string_1\n",
                "    push 15\n",
                "    call allocate_memory\n",
                "    mov rax, qword [string_1]\n",
                "    mov byte [rax+0], 'H'\n",
                "    mov byte [rax+1], 'e'\n",
                "    mov byte [rax+2], 'l'\n",
                "    mov byte [rax+3], 'l'\n",
                "    mov byte [rax+4], 'o'\n",
                "    mov byte [rax+5], ','\n",
                "    mov byte [rax+6], ' '\n",
                "    mov byte [rax+7], 'K'\n",
                "    mov byte [rax+8], 'a'\n",
                "    mov byte [rax+9], 't'\n",
                "    mov byte [rax+10], 'a'\n",
                "    mov byte [rax+11], 'n'\n",
                "    mov byte [rax+12], 'a'\n",
                "    mov byte [rax+13], '!'\n",
                "    mov byte [rax+14], 0\n",
            ]
            assert assembly == [
                "    ;; Calculate variable string length and push onto stack with string\n",
                "    push qword [string_1]\n",
                "    push qword [string_1]\n",
                "    call string_length\n",
                "    push qword [string_1]\n",
                "    ;; Keyword Func\n",
                "    call print_string\n"
            ]

    @pytest.mark.skip
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
                    "var_val": "Hello",
                    "is_const": True,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 db 'Hello', 0\n",
                    ]
                }
            }
            assert assembly == [
                "    ;; Calculate string length and push onto stack with string\n",
                "    push string_1\n",
                "    push string_1\n",
                "    call string_length\n",
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
                "    mov byte [rbx+rcx], al\n",
                "    ;; Calculate string length and push onto stack with string\n",
                "    push string_1\n",
                "    push string_1\n",
                "    call string_length\n",
                "    push string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
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
                    "var_val": "Hello",
                    "is_const": True,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 db 'Hello', 0\n",
                        "    len_1 equ $ - 5\n"
                    ]
                }
            }
            assert assembly == [
            ]


class TestCompilerChar:
    """
    All tests related to the char keyword.
    """

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
                    "var_val": "a",
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    char_1 db 'a', 0\n"
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
                    "var_val": "h",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    char_1 db 'h', 0\n",
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
                    "var_val": "A",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    char_1 db 'A', 0\n",
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


class TestCompilerUpdateChar:
    """
    All tests related to the updateChar function.
    """

    def test_update_char_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_update_char_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push variable string onto stack without length\n",
                "    push qword [string_1]\n",
                "    ;; Push number onto stack\n",
                "    push 0\n",
                "    ;; Push a raw char onto the stack\n",
                "    mov bl, [raw_char_1]\n",
                "    push bx\n",
                "    ;; Keyword Func\n",
                "    call update_char\n",
            ]


class TestCompilerCopyStr:
    """
    All tests related to the copyStr function.
    """

    def test_copy_str_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_copy_str_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section":  "var_1",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 5,
                    "var_val": "Hello",
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    string_1 dq 0\n"
                    ]
                },
                "y": {
                    "section":  "var_2",
                    "var_name": "string_2",
                    "var_type": "string",
                    "var_len": 5,
                    "var_val": "olleH",
                    "is_const": False,
                    "asm": [
                        "section .var_2 write\n",
                        "    string_2 dq 0\n"
                    ]
                }
            }
            assert assembly == [
                "    ;; Push variable string onto stack without length\n",
                "    push qword [string_2]\n",
                "    ;; Push variable string onto stack without length\n",
                "    push qword [string_1]\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mov byte cl, [rbx+0]\n",
                "    mov byte [rax+0], cl\n",
                "    mov byte cl, [rbx+1]\n",
                "    mov byte [rax+1], cl\n",
                "    mov byte cl, [rbx+2]\n",
                "    mov byte [rax+2], cl\n",
                "    mov byte cl, [rbx+3]\n",
                "    mov byte [rax+3], cl\n",
                "    mov byte cl, [rbx+4]\n",
                "    mov byte [rax+4], cl\n",
            ]


class TestCompilerBool:
    """
    All tests related to the bool keyword.
    """

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
                    "var_val": "false",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
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
                    "var_val": "true",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
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
                    "var_val": "true",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
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

    def test_bool_updated(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_bool_updated.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "x": {
                    "section": "var_1",
                    "var_name": "bool_1",
                    "var_type": "bool",
                    "var_len": 4,
                    "var_val": "true",
                    "is_const": False,
                    "asm": [
                        "section .var_1 write\n",
                        "    bool_1 dq 1\n",
                    ]
                }
            }
            assert assembly == [
                "    ;; Assign new bool to bool var\n",
                "    mov word [bool_1], 0\n",
            ]


class TestCompilerIfElse:
    """
    All tests related the if/else conditional block.  
    """

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


class TestCompilerLoop:
    """
    All tests related to the loop keywords.
    """

    def test_loop_up(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]

    def test_loop_down(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_down.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_0\n",
            ]

    def test_loop_from_ascending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_ascending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]

    def test_loop_from_descending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_descending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_0\n",
            ]

    def test_loop_up_and_down_not_nested(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up_down_not_nested.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 2\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 10\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 12\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_1\n",
            ]

    def test_loop_up_and_down_nested(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up_and_down_nested.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 2\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_1], 3\n",
                "    mov qword [loop_end_1], 0\n",
                "    ;; Loop down\n",
                "    loop_1:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 6\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_1]\n",
                "    mov rbx, [loop_end_1]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_1], rcx\n",
                "    mov qword [loop_end_1], rbx\n",
                "    jg loop_1\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]

    def test_loop_up_with_vars(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up_with_vars.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov rax, [number_1]\n",
                "    mov qword [loop_end_0], rax\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 6\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]

    def test_loop_down_with_vars(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_down_with_vars.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov rax, [number_1]\n",
                "    mov qword [loop_idx_0], rax\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 8\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_0\n",
            ]

    def test_loop_from_with_var_first_param(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_with_var_first_param.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov rax, [number_1]\n",
                "    mov qword [loop_idx_0], rax\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 8\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_0\n",
            ]

    def test_loop_from_with_var_second_param(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_with_var_second_param.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov rax, [number_1]\n",
                "    mov qword [loop_end_0], rax\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 8\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]


class TestCompilerLoopIdx:
    """
    All tests related accessing the loop index within the loops.
    """

    def test_loop_access_index_setup(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_index_access.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            compiler.compile()
            assert compiler.loop_idx_asm == [
                "section .loop_indices write\n",
                "    loop_idx_0 dq 0\n",
                "    loop_end_0 dq 0\n",
                "    loop_idx_1 dq 0\n",
                "    loop_end_1 dq 0\n",
            ]

    def test_loop_up(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up_access_index.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 11\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Push loop idx 0 onto stack\n",
                "    mov rax, [loop_idx_0]\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call printl_num\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]

    def test_loop_down(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_down_access_index.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 11\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Push loop idx 0 onto stack\n",
                "    mov rax, [loop_idx_0]\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call printl_num\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jg loop_0\n",
            ]

    def test_loop_from(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_access_index.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 11\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Push loop idx 0 onto stack\n",
                "    mov rax, [loop_idx_0]\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call printl_num\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jl loop_0\n",
            ]


class TestCompilerLoopInclusive:
    """
    All tests related to inclusive loops.
    """

    def test_loop_up_inclusive(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_up_inclusive.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jle loop_0\n",
            ]

    def test_loop_down_inclusive(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_down_inclusive.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jge loop_0\n",
            ]

    def test_loop_from_inclusive_ascending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_inclusive_ascending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 0\n",
                "    mov qword [loop_end_0], 3\n",
                "    ;; Loop up\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is below loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    inc rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jle loop_0\n",
            ]

    def test_loop_from_inclusive_descending(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_loop_from_inclusive_descending.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert assembly == [
                "    ;; Push loop start and end on stack\n",
                "    mov qword [loop_idx_0], 3\n",
                "    mov qword [loop_end_0], 0\n",
                "    ;; Loop down\n",
                "    loop_0:\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 7\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call printl_string\n",
                "    ;; Compare if counter is above loop end\n",
                "    mov rcx, [loop_idx_0]\n",
                "    mov rbx, [loop_end_0]\n",
                "    dec rcx\n",
                "    cmp rcx, rbx\n",
                "    mov qword [loop_idx_0], rcx\n",
                "    mov qword [loop_end_0], rbx\n",
                "    jge loop_0\n",
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
                    "int_type": "int64",
                    "var_len": 1,
                    "var_val": "1",
                    "is_const": True,
                    "asm": [
                        "section .var_1\n",
                        "    number_1 dq 1\n",
                    ]
                },
                "y": {
                    "section": "var_2",
                    "var_name": "string_1",
                    "var_type": "string",
                    "var_len": 14,
                    "var_val": "Hello, Katana!",
                    "is_const": True,
                    "asm": [
                        "section .var_2\n",
                        "    string_1 db 'Hello, Katana!', 0\n",
                    ]
                },
                "z": {
                    "section": "var_3",
                    "var_name": "char_1",
                    "var_type": "char",
                    "var_len": 1,
                    "var_val": "A",
                    "is_const": True,
                    "asm": [
                        "section .var_3\n",
                        "    char_1 db 'A', 0\n",
                    ]
                }
            }


class TestCompilerMacroKeyword:
    """
    Tests related to the macro keyword.
    """

    def test_macro_successfully_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_macro_replaces_successfully.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 17\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Push number onto stack\n",
                "    push 4\n",
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call print_num\n",
            ]

    def test_macro_successfully_used_more_than_once(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_macro_multiple_uses.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    ;; Push a raw string and length onto stack\n",
                "    push 17\n",
                "    push raw_string_1\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
                "    ;; Push number onto stack\n",
                "    push 3\n",
                "    ;; Push number onto stack\n",
                "    push 4\n",
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "    ;; Keyword Func\n",
                "    call print_num\n",
                "    ;; Push a raw string and length onto stack\n",
                "    push 17\n",
                "    push raw_string_2\n",
                "    ;; Keyword Func\n",
                "    call print_string\n",
            ]


class TestCompilerFunctions:
    """
    Tests related to the declaration and usage of functions.
    """

    def test_function_successfully_declared_and_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_fn_declaration_and_use.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()

            # TODO(map) The formatting on this function could be nicer
            assert compiler.user_func_asm["add"] == [
                "section .text\n",
                "    add:\n",
                "        ;; Get return address\n",
                "        pop rcx\n",
                "        ;; Get pointer to the args\n",
                "        pop rdx\n",
                "        ;; Get the pointer to the clean stack\n",
                "        mov r8, [rdx + 16]\n",
                "        ;; Get a function argument\n",
                "        mov r9, [rdx + 0]\n",
                "        ;; Get a function argument\n",
                "        mov r10, [rdx + 8]\n",
                "        ;; Push return for this method onto the stack to save a reference\n",
                "        push rcx\n",
                "    ;; Push number onto stack\n",
                "    push r9\n",
                "    ;; Push number onto stack\n",
                "    push r10\n",
                "    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    call check_int_64_overflow\n",
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
                "    add rax, rbx\n",
                "    push rax\n",
                "        ;; Get return value before pointer reset\n",
                "        pop rax\n",
                "        ;; Get return address before pointer reset\n",
                "        pop rcx\n",
                "        ;; Reset the pointer to the clean part of the stack\n",
                "        mov rsp, r8\n",
                "        ;; Push return value onto stack\n",
                "        push rax\n",
                "        ;; Push return address onto stack\n",
                "        push rcx\n",
                "        ret\n",
            ]

            assert assembly == [
                "    ;; Push pointer to current stack position onto stack\n",
                "    push rsp\n",
                "    ;; Push arg 1\n",
                "    push 3\n",
                "    ;; Push arg 2\n",
                "    push 4\n",
                "    ;; Push pointer to the start of the args\n",
                "    push rsp\n",
                "    ;; Call add function\n",
                "    call add\n"
            ]
