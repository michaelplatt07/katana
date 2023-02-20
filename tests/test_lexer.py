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
    InvalidConcatenationException,
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


class TestComments:
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


class TestLexerWellFormattedPrograms:
    """
    These tests are for programs that are well formatted, no extra spaces,
    stuff like that.
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
        program = Program(["`;"])
        lexer = Lexer(program)
        with pytest.raises(InvalidTokenException, match="Invalid token '`' at 1:0."):
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
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW),
        ]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    def test_main_function_keyword(self):
        """
        Ensures the main method keyword is lexed correctly.
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

    def test_main_should_error_all_one_line(self):
        """
        Tests the continuation logic if everything is on one line.
        """
        program = Program(["main() {print(1+2)}\n"])
        lexer = Lexer(program)
        with pytest.raises(NoTerminatorError, match="Line 1:18 must end with a semicolon."):
            lexer.lex()

    def test_main_function_should_error_multi_line(self):
        """
        If there is no semicolon ending the line, an error should be raised for
        multiline program.
        """
        program = Program(["main() {\n", "print(1+2)\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(NoTerminatorError, match="Line 2:10 must end with a semicolon."):
            lexer.lex()

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

    def test_int_16_variable_declaration(self):
        """
        Tests that declaring an int16 variable correctly declares the
        appropriate tokens to be parsed.
        """
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

    def test_int_16_variable_usage(self):
        """
        Tests that declaring and using an int16 variable correctly lexes to the
        appropriate tokens.
        """
        program = Program(["main() {\n", "int16 x = 3;\n", "print(x);\n", "}\n"])
        token_list = get_main_tokens() + [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int16", ULTRA_HIGH),
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

    def test_invalid_int_16_variable_name_with_underscore(self):
        """
        Test to make sure if a variable is anything other than alpha numeric
        an error is raised.
        """
        program = Program(
            ["main() {\n", "int16 var_with_underscore = 3;\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(InvalidTokenException, match="Invalid token '_' at 2:9."):
            lexer.lex()

    def test_invalid_int_16_variable_name_starts_with_number(self):
        """
        Test to make sure that a variable name starting with a number raises
        an exception.
        """
        program = Program(
            ["main() {\n", "int16 1_var = 3;\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(InvalidVariableNameError, match="Variable name at 2:6 cannot start with digit."):
            lexer.lex()

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

    def test_invalid_character_variable_declaration_raises_exception(self):
        """
        Tests that anything other than a char in the format 'a' is not valid.
        """
        program = Program(["main() {\n", "char x = 'hi';\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(InvalidCharException, match="Invalid declaration of `char` at 2:11."):
            lexer.lex()

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

    def test_string_variable_usage(self):
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

    def test_else_with_no_if_raises_error(self):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        program = Program(["main() {\n", "else {\n", "print(\"low\");\n", "}\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(UnpairedElseError, match="else at 2:0 does not have a matching if block."):
            lexer.lex()

    def test_else_with_something_between_raises_error(self):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        program = Program(["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "}\n", "print(\"really bad\");\n", "else {\n", "print(\"low\");\n", "}\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(BadFormattedLogicBlock, match="Incorrectly formatted else statement at 6:0. Cannot have code between if/else block."):
            lexer.lex()

    def test_else_with_something_between_same_line_raises_error(self):
        """
        If the `else` keyword is present without the `if` keyword we get an
        exception in the lexer.
        """
        program = Program(["main() {\n", "if (1 > 2) {\n", "print(\"high\");\n", "}\n",  "print(\"really bad\");else {\n", "print(\"low\");\n", "}\n", "}\n"])
        lexer = Lexer(program)
        with pytest.raises(BadFormattedLogicBlock, match="Incorrectly formatted else statement at 5:0. Cannot have code between if/else block."):
            lexer.lex()

    def test_nested_if_else_with_bad_line(self):
        """
        Ensures that the nested if/else block that are improperly formatted get
        flagged instead of outer blocks.
        """
        program = Program([
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
        ])
        lexer = Lexer(program)
        with pytest.raises(BadFormattedLogicBlock, match="Incorrectly formatted else statement at 8:0. Cannot have code between if/else block."):
            lexer.lex()

    def test_nested_else_without_if(self):
        """
        Ensures that the inner `else` without an if block gets flagged as the
        unpaired else instead of the outer else.
        """
        program = Program([
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
        ])
        lexer = Lexer(program)
        with pytest.raises(UnpairedElseError, match="else at 4:0 does not have a matching if block."):
            lexer.lex()

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


class TestQuotationCharacter:

    def test_quote_character(self):
        program = Program(["\"test string\";\n"])
        token_list = [
            Token(STRING_TOKEN_TYPE, 0, 0, "test string", LOW),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
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


class TestStringExtension:

    def test_extending_string_with_a_single_char_succeeds(self):
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
