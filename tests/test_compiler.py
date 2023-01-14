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
                "    push 3\n",
            ]


class TestCompilerMathematics:

    def test_simple_add(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_add.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    push 1\n",
                "    push 2\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
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
                "    push 1\n",
                "    push 2\n",
                "    ;; Subtract\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    sub rbx, rax\n",
                "    push rbx\n",
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
                "    push 1\n",
                "    push 2\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
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
                "    push 1\n",
                "    push 2\n",
                "    ;; Divide\n",
                "    pop rbx\n",
                "    pop rax\n",
                "    div rbx\n",
                "    push rax\n",
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
                "    push 1\n",
                "    push 2\n",
                "    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n",
                "    push 3\n",
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
                "    push 1\n",
                "    push 2\n",
                "    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n",
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
                "    push 3\n",
                "    ;; Keyword Func\n",
                "    call print\n",
            ]

    def test_main_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_main.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    push 14\n",
                "    push string_1\n",
                "    ;; Keyword Func\n",
                "    call print\n",
            ]

    def test_assignment_keyword(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assignment.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "var_1": [
                    "section .var_1\n",
                    "    number_1 dw 3\n"
                ]
            }
            assert assembly == [
            ]

    @pytest.mark.skip
    def test_assignment_keyword_used(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_assignment_used.ktna") as f:
            compiler = get_compiler_class(f.readlines())
            assembly = compiler.get_assembly()
            assert compiler.variables == {
                "var_1": [
                    "section .var_1\n",
                    "    number_1 dw 3\n"
                ]
            }
            assert assembly == [
            ]


class TestCompilerString:

    def test_string(self):
        curr_dir = os.getcwd()
        with open(curr_dir + "/tests/test_programs/sample_string.ktna") as f:
            assembly = get_assembly_for_program(f.readlines())
            assert assembly == [
                "    push 13\n",
                "    push string_1\n",
            ]
