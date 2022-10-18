import pytest

from katana.katana import (
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    Lexer,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    Token,
    HIGH,
    MEDIUM,
    LOW
)


class TestComments:
    """Testing to make sure comments are picked up appropriately."""

    def test_single_line_comment(self):
        program = "// Comment\n"
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, "// Comment", LOW),
                      Token(EOF_TOKEN_TYPE, 11, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_after_line(self):
        program = "1 + 2 // Comment\n"
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                      Token(COMMENT_TOKEN_TYPE, 6, "// Comment", LOW),
                      Token(EOF_TOKEN_TYPE, 17, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_before_program(self):
        program = "// Comment\n1 + 2\n"
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, "// Comment", LOW),
                      Token(NUM_TOKEN_TYPE, 11, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 13, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 15, "2", LOW),
                      Token(EOF_TOKEN_TYPE, 17, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_after_program(self):
        program = "1 + 2\n// Comment\n"
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                      Token(COMMENT_TOKEN_TYPE, 6, "// Comment", LOW),
                      Token(EOF_TOKEN_TYPE, 17, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerWellFormattedPrograms:
    """
    These tests are for programs that are well formatted, no extra spaces,
    stuff like that.
    """

    def test_lex_single_digit_number(self):
        program = "3"
        token_list = [Token(NUM_TOKEN_TYPE, 0, "3", LOW),
                      Token(EOF_TOKEN_TYPE, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            ("12", [Token(NUM_TOKEN_TYPE, 1, "12", LOW),
             Token(EOF_TOKEN_TYPE, 2, "EOF", LOW)]),
            ("345", [Token(NUM_TOKEN_TYPE, 2, "345", LOW),
             Token(EOF_TOKEN_TYPE, 3, "EOF", LOW)]),
        ],
    )
    def test_lex_multi_digit_number(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            (
                "1 + 2",
                [
                    Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
            (
                "3 + 4",
                [
                    Token(NUM_TOKEN_TYPE, 0, "3", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "4", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_simple_add(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            (
                "1 - 2",
                [
                    Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
            (
                "3 - 4",
                [
                    Token(NUM_TOKEN_TYPE, 0, "3", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "4", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_simple_subtract(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            (
                "1 + 2 - 3",
                [
                    Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                    Token(MINUS_TOKEN_TYPE, 6, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 8, "3", LOW),
                    Token(EOF_TOKEN_TYPE, 9, "EOF", LOW),
                ],
            ),
            (
                "3 - 4 + 5",
                [
                    Token(NUM_TOKEN_TYPE, 0, "3", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, "4", LOW),
                    Token(PLUS_TOKEN_TYPE, 6, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 8, "5", LOW),
                    Token(EOF_TOKEN_TYPE, 9, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_combined_addition_and_subtraction(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            (
                "1 * 2",
                [
                    Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                    Token(MULTIPLY_TOKEN_TYPE, 2, "*", HIGH),
                    Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lexer_simple_multiply(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize(
        "program,token_list",
        [
            (
                "1 / 2",
                [
                    Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                    Token(DIVIDE_TOKEN_TYPE, 2, "/", HIGH),
                    Token(NUM_TOKEN_TYPE, 4, "2", LOW),
                    Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lexer_simple_divide(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerBadFormat:
    """
    Testing the lexer with programs that are poorly formatted, like extra
    spaces.
    """

    def test_lex_extra_spaces(self):
        program = "     1 -      2      "
        token_list = [
            Token(NUM_TOKEN_TYPE, 5, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 7, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 14, "2", LOW),
            Token(EOF_TOKEN_TYPE, 21, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()
