from unittest.mock import patch
import pytest

from katana.katana import (
    Lexer,
    Program,
    Token,
    ASSIGNMENT_TOKEN_TYPE,
    BOOLEAN_TOKEN_TYPE,
    CHARACTER_TOKEN_TYPE,
    COMMA_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EQUAL_TOKEN_TYPE,
    GREATER_THAN_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    LESS_THAN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RANGE_INDICATION_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    STRING_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    VARIABLE_REFERENCE_TOKEN_TYPE,
    LOW,
    HIGH,
    MEDIUM,
    VERY_HIGH,
    ULTRA_HIGH,
    BadFormattedLogicBlock,
    InvalidCharException,
    InvalidTokenException,
    InvalidVariableNameError,
    NoTerminatorError,
    UnclosedParenthesisError,
    UnclosedQuotationException,
    UnknownKeywordError,
    UnpairedElseError
)


def get_main_tokens():
    return [
        Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
        Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
        Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
        Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
    ]


class TestLexerComments:
    """Testing to make sure comments are picked up appropriately."""

    def test_single_line_comment(self):
        program = Program(["// Comment\n"])
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, 0, "// Comment", LOW),
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
                      Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_before_program(self):
        program = Program(["// Comment\n", "1 + 2;\n"])
        token_list = [Token(COMMENT_TOKEN_TYPE, 0, 0, "// Comment", LOW),
                      Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
                      Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_comment_after_program(self):
        program = Program(["1 + 2;\n", "// Comment\n"])
        token_list = [Token(NUM_TOKEN_TYPE, 0, 0, "1", LOW),
                      Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
                      Token(NUM_TOKEN_TYPE, 4, 0, "2", LOW),
                      Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
                      Token(COMMENT_TOKEN_TYPE, 0, 1, "// Comment", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerBasicLexingAbilities:
    """
    These are not complete programs as they don't have a `main` method but
    rather designed to be small snippets of code to ensure the lexing works as
    expected.
    """

    def test_lex_single_digit_number(self):
        program = Program(["3;\n"])
        token_list = [Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
                      Token(EOL_TOKEN_TYPE, 1, 0, ";", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @ pytest.mark.parametrize(
        "lines,token_list",
        [
            (["12;\n"], [Token(NUM_TOKEN_TYPE, 0, 0, "12", LOW),
             Token(EOL_TOKEN_TYPE, 2, 0, ";", LOW),
             Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)]),
            (["345;\n"], [Token(NUM_TOKEN_TYPE, 0, 0, "345", LOW),
             Token(EOL_TOKEN_TYPE, 3, 0, ";", LOW),
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
                    Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
                ],
            ),
        ],
    )
    def test_lexer_simple_divide(self, lines, token_list):
        program = Program(lines)
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerUncommonFormatting:
    """
    Tests to check if the lexer can handle code snippets that have extra
    spaces, additional new lines between different snippets, etc.
    """

    def test_lex_extra_spaces(self):
        program = Program(["     1 -      2      ;\n"])
        token_list = [
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 7, 0, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 14, 0, "2", LOW),
            Token(EOL_TOKEN_TYPE, 21, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerParenthesis:
    """
    Tests that parenthesis in various places in the program get lexed
    appropriately.
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
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_unclosed_paren_error(self, mock_print):
        program = Program(["1 + (2 + 3;\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["1 + (2 + 3;\n"], 4, UnclosedParenthesisError(0, 4))

    @patch("katana.katana.print_exception_message")
    def test_unclosed_paren_error_other_side(self, mock_print):
        program = Program(["1 + 2) + 3;\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["1 + 2) + 3;\n"], 5, UnclosedParenthesisError(0, 5))

class TestLexerEndOfLineSemicolon:
    """
    Tests to ensure that the lines that should end in a semicolon do so.
    """

    def test_line_ends_with_semicolon(self):
        program = Program(["3 + 4;\n"])
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 0, "4", LOW),
            Token(EOL_TOKEN_TYPE, 5, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_error_if_line_ends_without_semicolon(self, mock_print):
        program = Program(["3 + 4\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["3 + 4\n"], 5, NoTerminatorError(0, 5))

    @patch("katana.katana.print_exception_message")
    def test_error_if_later_line_ends_without_semicolon(self, mock_print):
        code = ["main() {\n", "int16 x = 16;\n", "print(x)\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 7, NoTerminatorError(2, 8))

class TestLexerInvalidTokenException:

    @patch("katana.katana.print_exception_message")
    def test_invalid_token_raises_exception(self, mock_print):
        """
        Ensures that if an unknown token shows up an exception is raised.
        """
        program = Program(["`;"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["`;"], 0, InvalidTokenException(0, 0, "`"))


class TestLexerInvalidKeyword:
    """
    Tests to ensure that an invalid keyword gets flagged by the lexer.
    """

    @patch("katana.katana.print_exception_message")
    def test_invalid_keyword(self, mock_print):
        """
        Ensuring an error is raised if an unrecognized keyword is in program.
        """
        program = Program(["foo(3+4);\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["foo(3+4);\n"], 2, UnknownKeywordError(0, 0, "foo"))


class TestLexerPrintKeyword:
    """
    All tests related to using the print keyword.
    """

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
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_printl_function_keyword(self):
        """
        Ensures the main method keyword is lexed correctly.
        """
        program = Program(["main() {\n", "printl(1+2);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "printl", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 6, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 7, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 8, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 9, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerMainKeyword:
    """
    All tests related to the main keyword.
    """

    def test_main_function_keyword_one_line(self):
        """
        Ensures the main method keyword is lexed correctly if everything is
        kept to a single line.
        """
        program = Program(["main() {print(1+2);};\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 8, 0, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 14, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 15, 0, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 16, 0, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 17, 0, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 18, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 19, 0, "}", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 20, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_main_function_with_new_lines(self):
        """
        Same program as above test but with new lines.
        """
        program = Program(["main() {\n", "print(1+2);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 6, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 7, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 9, 1, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 10, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerIntKeyword:
    """
    All tests related to all the different type of int declarations.
    """

    def test_int_64_variable_declaration(self):
        """
        Tests that declaring an int64 variable correctly declares the
        appropriate tokens to be parsed.
        """
        program = Program(["main() {\n", "int64 x = 3;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_int_64_variable_referenced(self):
        """
        Tests that declaring and using an int64 variable correctly lexes to the
        appropriate tokens.
        """
        program = Program(["main() {\n", "int64 x = 3;\n", "print(x);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_invalid_int_64_variable_name_with_underscore(self, mock_print):
        """
        Test to make sure if a variable is anything other than alpha numeric
        an error is raised.
        """
        code = ["main() {\n", "int64 var_with_underscore = 3;\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 9, InvalidTokenException(1, 9, "_"))

    @patch("katana.katana.print_exception_message")
    def test_invalid_int_64_variable_name_starts_with_number(self, mock_print):
        """
        Test to make sure that a variable name starting with a number raises
        an exception.
        """
        code = ["main() {\n", "int64 1_var = 3;\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 6, InvalidVariableNameError(1, 6))

    def test_const_int_variable_delcaration(self):
        """
        Test to make sure that if `const` is used in the variable declaration
        we can lex it correctly.
        """
        program = Program(["main() {\n", "const int64 x = 0;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "const", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 6, 1, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 12, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 14, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 16, 1, "0", LOW),
            Token(EOL_TOKEN_TYPE, 17, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert lexer.lex() == token_list

    def test_int_8_variable_declaration(self):
        program = Program(["main() {\n", "int8 x = 3;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_int_16_variable_declaration(self):
        program = Program(["main() {\n", "int16 x = 3;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int16", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_int_32_variable_declaration(self):
        program = Program(["main() {\n", "int32 x = 3;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int32", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerCharKeyword:
    """
    All tests related to the char keyword.
    """

    def test_character_variable_declaration(self):
        """
        Tests that declaring a character variable correctly declares the
        appropriate tokens to be parsed.
        """
        program = Program(["main() {\n", "char x = 'h';\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "char", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(CHARACTER_TOKEN_TYPE, 10, 1, "h", LOW),
            Token(EOL_TOKEN_TYPE, 12, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_invalid_character_variable_declaration_raises_exception(self, mock_print):
        """
        Tests that anything other than a char in the format 'a' is not valid.
        """
        code = ["main() {\n", "char x = 'hi';\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 11, InvalidCharException(1, 11))

    def test_char_variable_reference(self):
        """
        Tests the referencing a char is correctly lexed.
        """
        program = Program(["main() {\n", "    const char x = 'A';\n", "    print(x);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "const", 4),
            Token(KEYWORD_TOKEN_TYPE, 10, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 15, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 17, 1, "=", 2),
            Token(CHARACTER_TOKEN_TYPE, 20, 1, "A", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 9, 2, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 10, 2, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 12, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerString:
    """
    All tests related to the string keyword.
    """

    def test_string_variable_declaration(self):
        """
        Tests that declaring a string variable correctly declares the
        appropriate tokens to be parsed.
        """
        program = Program(["main() {\n", "string x = \"hello\";\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_string_variable_referenced(self):
        """
        Confirms that referencing the string appropriately works.
        """
        program = Program(["main() {\n", "string x = \"hello\";\n", "print(x);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerBoolKeyword:
    """
    All tests related to the bool keyword.
    """

    def test_bool_variable_declaration(self):
        """
        Tests that declaring a string variable correctly declares the
        appropriate tokens to be parsed.
        """
        program = Program(["main() {\n", "bool x = false;\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "bool", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(BOOLEAN_TOKEN_TYPE, 9, 1, "false", LOW),
            Token(EOL_TOKEN_TYPE, 14, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_bool_variable_referenced(self):
        program = Program(["main() {\n", "bool x = false;\n", "print(x);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "bool", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(BOOLEAN_TOKEN_TYPE, 9, 1, "false", LOW),
            Token(EOL_TOKEN_TYPE, 14, 1, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerIfElseKeyword:
    """
    All tests related to the if/else logical operators.
    """

    def test_if_keyword_success(self):
        """
        Test to make sure the `if` keyword by itself correctly lexes.
        """
        program = Program(["main() {\n", "if (1 > 0) {\n", "print(\"low\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "if", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "1", LOW),
            Token(GREATER_THAN_TOKEN_TYPE, 6, 1, ">", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "0", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 9, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 11, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "low", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_if_keyword_less_than_operator(self):
        """
        Test to make sure the less than operator works and is lexed.
        """
        program = Program(["main() {\n", "if (1 < 0) {\n", "print(\"low\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "if", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "1", LOW),
            Token(LESS_THAN_TOKEN_TYPE, 6, 1, "<", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "0", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 9, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 11, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "low", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_if_keyword_equal_operator(self):
        """
        Test to make sure equal operator works and is lexed.
        """
        program = Program(["main() {\n", "if (0 == 0) {\n", "print(\"low\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "if", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "0", LOW),
            Token(EQUAL_TOKEN_TYPE, 6, 1, "==", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 1, "0", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 12, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "low", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_else_with_no_if_raises_error(self, mock_print):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        code = ["main() {\n", "else {\n", "print(\"low\");\n", "}\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 1, UnpairedElseError(1, 0))

    @patch("katana.katana.print_exception_message")
    def test_else_with_something_between_raises_error(self, mock_print):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        code = ["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "}\n", "print(\"really bad\");\n", "else {\n", "print(\"low\");\n", "}\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 5, BadFormattedLogicBlock(5, 0))

    @patch("katana.katana.print_exception_message")
    def test_else_with_something_between_same_line_raises_error(self, mock_print):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        code = ["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "}\n",  "print(\"really bad\");else {\n", "print(\"low\");\n", "}\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 4, BadFormattedLogicBlock(4, 0))

    @patch("katana.katana.print_exception_message")
    def test_nested_if_else_with_bad_line(self, mock_print):
        """
        Ensures that the nested if/else block that are improperly formatted get
        flagged instead of outer blocks.
        """
        code = [
            "main() {\n",
            "if (1 == 2) {\n",
            "print(\"first if\");\n",
            "if (2 == 3){\n",
            "print(\"second if\");\n",
            "}\n",
            "print(\"bad line\");\n",
            "else {\n",
            "print(\"second else\");\n",
            "}\n",
            "else {\n",
            "print(\"first else\");\n",
            "}\n",
            "}\n",
            "}\n"
        ]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 7, BadFormattedLogicBlock(7, 0))

    @patch("katana.katana.print_exception_message")
    def test_nested_else_without_if(self, mock_print):
        """
        Ensures that the inner `else` without an if block gets flagged as the
        unpaired else instead of the outer else.
        """
        code = [
            "main() {\n",
            "if (1 == 2) {\n",
            "print(\"first if\");\n",
            "else {\n",
            "print(\"second else\");\n",
            "}\n",
            "else {\n",
            "print(\"first else\");\n",
            "}\n",
            "}\n"
        ]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 3, UnpairedElseError(3, 0))

    def test_if_else_success(self):
        """
        If there is an `if` paired with an `else` the lexer succeeds.
        """
        program = Program(["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "}\n", "else {\n", "print(\"low\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "if", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "1", LOW),
            Token(GREATER_THAN_TOKEN_TYPE, 6, 1, ">", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 9, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 11, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "high", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 12, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 13, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 4, "else", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 5, 4, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 5, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 5, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 5, "low", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 5, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 5, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 6, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 7, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 8, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_if_else_on_same_line_success(self):
        """
        If there is an `if` paired with an `else` the lexer succeeds.
        """
        program = Program(["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "} else {\n", "print(\"low\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "if", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "1", LOW),
            Token(GREATER_THAN_TOKEN_TYPE, 6, 1, ">", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 9, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 11, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "high", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 12, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 13, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),

            Token(KEYWORD_TOKEN_TYPE, 2, 3, "else", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 3, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 4, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 4, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 4, "low", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 4, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 12, 4, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 5, "}", VERY_HIGH),

            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 6, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 7, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerLoopKeyword:
    """
    All tests related to the various loop keywords and how they are parse.
    """

    def test_basic_loop_up_keyword(self):
        program = Program(["main() {\n", "loopUp(3) {\n",  "print(\"looping\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "loopUp", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 6, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 7, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 8, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 10, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "looping", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 16, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_basic_loop_down_keyword(self):
        program = Program(["main() {\n", "loopDown(3) {\n",  "print(\"looping\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "loopDown", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 8, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 9, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 12, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "looping", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 16, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_basic_loop_from_keyword(self):
        program = Program(["main() {\n", "loopFrom(0..3) {\n",  "print(\"looping\");\n", "}\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "loopFrom", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 8, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 9, 1, "0", LOW),
            Token(RANGE_INDICATION_TOKEN_TYPE, 10, 1, "..", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 13, 1, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 15, 1, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 6, 2, "looping", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 16, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerCharAt:
    """
    All tests related to the charAt function.
    """

    def test_char_at_function(self):
        program = Program(["main() {\n", "charAt(\"Hello\", 3);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "charAt", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 6, 1, "(", VERY_HIGH),
            Token(STRING_TOKEN_TYPE, 7, 1, "Hello", LOW),
            Token(COMMA_TOKEN_TYPE, 14, 1, ",", LOW),
            Token(NUM_TOKEN_TYPE, 16, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 17, 1, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerQuotationCharacter:
    """
    All tests related to useing the quotation character.
    """

    def test_quote_character(self):
        program = Program(["\"test string\";\n"])
        token_list = [
            Token(STRING_TOKEN_TYPE, 0, 0, "test string", LOW),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @patch("katana.katana.print_exception_message")
    def test_exception_raised_with_no_closing_quote_eol(self, mock_print):
        program = Program(["\"test string;\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["\"test string;\n"], 12, UnclosedQuotationException(0, 12, "test string"))

    @patch("katana.katana.print_exception_message")
    def test_exception_raised_with_no_closing_quote_new_line(self, mock_print):
        program = Program(["\"test string\n"])
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(["\"test string\n"], 12, UnclosedQuotationException(0, 12, "test string"))


class TestLexerUpdateCharKeyword:
    """
    All tests related to updating a char through the updateChar method.
    """
    def test_update_char_can_be_parsed(self):
        program = Program(["main() {\n", "string x = \"Hello\";\n", "updateChar(x, 0, 'Q');\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "Hello", LOW),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "updateChar", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 11, 2, "x", LOW),
            Token(COMMA_TOKEN_TYPE, 12, 2, ",", LOW),
            Token(NUM_TOKEN_TYPE, 14, 2, "0", LOW),
            Token(COMMA_TOKEN_TYPE, 15, 2, ",", LOW),
            Token(CHARACTER_TOKEN_TYPE, 18, 2, "Q", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 20, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 21, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestCopyString:
    """
    All tests related to using the copyStr method.
    """

    def test_keyword_str_copy(self):
        program = Program(["main() {\n", "string x = \"Hello\";\n", "string y = \"Katana\";\n", "copyStr(x, y);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "Hello", LOW),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 2, "y", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 2, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 2, "Katana", LOW),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 0, 3, "copyStr", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 7, 3, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 8, 3, "x", LOW),
            Token(COMMA_TOKEN_TYPE, 9, 3, ",", LOW),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 11, 3, "y", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 12, 3, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 13, 3, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerStringConcatenation:
    """
    All tests related to conatenating strings.
    """

    def test_string_concatenation_with_char(self):
        program = Program(["main() {\n", "string x = \"Hello\";\n", "x = x + '!';\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "Hello", LOW),
            Token(EOL_TOKEN_TYPE, 18, 1, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 0, 2, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 2, "=", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 4, 2, "x", 0),
            Token(PLUS_TOKEN_TYPE, 6, 2, "+", 1),
            Token(CHARACTER_TOKEN_TYPE, 9, 2, "!", 0),
            Token(EOL_TOKEN_TYPE, 11, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()


class TestLexerDotOperator:
    """
    All tests related to using the dot operator in the program.
    """

    @patch("katana.katana.print_exception_message")
    def test_single_dot_raises_error(self, mock_print):
        code = ["main() {\n", "1.2\n", "}\n"]
        program = Program(code)
        lexer = Lexer(program)
        with pytest.raises(SystemExit):
            lexer.lex()
        mock_print.assert_called_with(code, 1, InvalidTokenException(1, 1, "."))
