from typing import NewType
import pytest

from katana.katana import (
    LEFT_CURL_BRACE_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    Lexer,
    Program,
    Token,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    STRING_TOKEN_TYPE,
    InvalidTokenException,
    LOW,
    HIGH,
    MEDIUM,
    VERY_HIGH,
    ULTRA_HIGH,
    NoTerminatorError,
    UnclosedParenthesisError,
    UnclosedQuotationException,
    UnknownKeywordError,
)


class TestComments:
    """Testing to make sure comments are picked up appropriately."""

    def test_single_line_comment(self):
        program = Program(["// Comment\n"])
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, 0, "// Comment", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 10, 0, "\n", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_after_line(self):
        program = Program(["1 + 2; // Comment\n"])
        token_list = [Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                      Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                      Token(COMMENT_TOKEN_TYPE, 7, 0, "// Comment", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 17, 0, "\n", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_before_program(self):
        program = Program(["// Comment\n", "1 + 2;\n"])
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, 0, "// Comment", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 10, 0, "\n", LOW),
                      Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
                      Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 6, 1, "\n", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_after_program(self):
        program = Program(["1 + 2;\n", "// Comment\n"])
        token_list = [Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                      Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                      Token(COMMENT_TOKEN_TYPE, 0, 1, "// Comment", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 10, 1, "\n", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerWellFormattedPrograms:
    """
    These tests are for programs that are well formatted, no extra spaces,
    stuff like that.
    """

    def test_lex_single_digit_number(self):
        program = Program(["3;\n"])
        token_list = [Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
                      Token(EOL_TOKEN_TYPE, 1, 0, ";", LOW),
                      Token(NEW_LINE_TOKEN_TYPE, 2, 0, "\n", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (["12;\n"], [Token(NUM_TOKEN_TYPE, 0, 0, "12", LOW),
             Token(EOL_TOKEN_TYPE, 2, 0, ";", LOW),
             Token(NEW_LINE_TOKEN_TYPE, 3, 0, "\n", LOW),
             Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]),
            (["345;\n"], [Token(NUM_TOKEN_TYPE, 0, 0, "345", LOW),
             Token(EOL_TOKEN_TYPE, 3, 0, ";", LOW),
             Token(NEW_LINE_TOKEN_TYPE, 4, 0, "\n", LOW),
             Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]),
        ],
    )
    def test_lex_multi_digit_number(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (
                ["1 + 2;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
            (
                ["3 + 4;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "4", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_simple_add(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (
                ["1 - 2;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, 0, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
            (
                ["3 - 4;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, 0, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "4", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_simple_subtract(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (
                ["1 + 2 - 3;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                    Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                    Token(MINUS_TOKEN_TYPE, 6, 0, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 8, 0, "3", LOW),
                    Token(EOL_TOKEN_TYPE, 9, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 10, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
            (
                ["3 - 4 + 5;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
                    Token(MINUS_TOKEN_TYPE, 2, 0, "-", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 4, 0, "4", LOW),
                    Token(PLUS_TOKEN_TYPE, 6, 0, "+", MEDIUM),
                    Token(NUM_TOKEN_TYPE, 8, 0, "5", LOW),
                    Token(EOL_TOKEN_TYPE, 9, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 10, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lex_combined_addition_and_subtraction(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (
                ["1 * 2;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                    Token(MULTIPLY_TOKEN_TYPE, 2, 0, "*", HIGH),
                    Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lexer_simple_multiply(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (
                ["1 / 2;\n"],
                [
                    Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                    Token(DIVIDE_TOKEN_TYPE, 2, 0, "/", HIGH),
                    Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                    Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                    Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lexer_simple_divide(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerBadFormat:
    """
    Testing the lexer with programs that are poorly formatted, like extra
    spaces.
    """

    def test_lex_extra_spaces(self):
        program = Program(["     1 -      2      ;\n"])
        token_list = [
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 7, 0, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 14, 0, "2", LOW),
            Token(EOL_TOKEN_TYPE, 21, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 22, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerParenthesis:
    """
    Testing that the parenthesis tokens get lexed correctly.
    """

    def test_paren_with_add_only(self):
        program = Program(["1 + (2 + 3);\n"])
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 5, 0, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 7, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 0, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 11, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 12, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_paren_with_add_and_mul(self):
        program = Program(["(1 + 2) * 3;\n"])
        token_list = [
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 1, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 3, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, 0, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 0, ")", VERY_HIGH),
            Token(MULTIPLY_TOKEN_TYPE, 8, 0, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 12, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_unclosed_paren_error(self):
        program = Program(["1 + (2 + 3;\n"])
        lexer = Lexer(program)
        with pytest.raises(UnclosedParenthesisError, match="Unclosed parenthesis at 1:4."):
            lexer.lex()

    def test_unclosed_paren_error_other_side(self):
        program = Program(["1 + 2) + 3;\n"])
        lexer = Lexer(program)
        with pytest.raises(UnclosedParenthesisError, match="Unclosed parenthesis at 1:5."):
            lexer.lex()


class TestEndOfLineSemicolon:

    def test_line_ends_with_semicolon(self):
        program = Program(["3 + 4;\n"])
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 0, "4", LOW),
            Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 6, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_error_if_line_ends_without_semicolon(self):
        program = Program(["3 + 4\n"])
        lexer = Lexer(program)
        with pytest.raises(NoTerminatorError, match="Line 1:5 must end with a semicolon."):
            lexer.lex()


class TestInvalidTokenException:

    def test_invalid_token_raises_exception(self):
        """
        Ensures that if an unknown token shows up an exception is raised.
        """
        program = Program(["';"])
        lexer = Lexer(program)
        with pytest.raises(InvalidTokenException, match="Invalid token ''' at 1:0."):
            lexer.lex()


class TestKeyword:

    def test_invalid_keyword(self):
        """
        Ensuring an error is raised if an unrecognized keyword is in program.
        """
        program = Program(["foo(3+4);\n"])
        lexer = Lexer(program)
        with pytest.raises(UnknownKeywordError, match="Unknown keyword 'foo' at 1:0 in program."):
            lexer.lex()

    def test_print_function_keyword(self):
        """
        Ensures the print keyword for the function is parsed.
        """
        program = Program(["print(3 + 4);\n"])
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 6, 0, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 8, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 10, 0, "4", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 0, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 13, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_main_function_keyword(self):
        """
        Ensures the main method keyword is lexed correctly.
        """
        program = Program(["main() {print(1+2);};\n"])
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 8, 0, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 14, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 15, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 16, 0, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 17, 0, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 18, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 19, 0, "}", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 20, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 21, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestQuotationCharacter:

    def test_quote_character(self):
        program = Program(["\"test string\";\n"])
        token_list = [
            Token(STRING_TOKEN_TYPE, 0, 0, "test string", LOW),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 14, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_exception_raised_with_no_closing_quote_eol(self):
        program = Program(["\"test string;\n"])
        lexer = Lexer(program)
        with pytest.raises(UnclosedQuotationException, match="Unclosed quotation mark for 'test string' at 1:12"):
            lexer.lex()

    def test_exception_raised_with_no_closing_quote_new_line(self):
        program = Program(["\"test string\n"])
        lexer = Lexer(program)
        with pytest.raises(UnclosedQuotationException, match="Unclosed quotation mark for 'test string' at 1:12"):
            lexer.lex()
