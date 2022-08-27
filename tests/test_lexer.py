import pytest

from katana.katana import MINUS_TOKEN_TYPE, NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE, Lexer, Token, EOF_TOKEN_TYPE

class TestLexerWellFormattedPrograms:
    """
    These tests are for programs that are well formatted, no extra spaces, stuff
    like that.
    """

    def test_lex_single_digit_number(self):
        program = "3"
        token_list = [Token(NUM_TOKEN_TYPE, 0, "3"), Token(EOF_TOKEN_TYPE, 1, "EOF")]
        lexer = Lexer(program)
        assert token_list == lexer.lex()

    @pytest.mark.parametrize("program,token_list", [
        ("12", [Token(NUM_TOKEN_TYPE, 1, "12"), Token(EOF_TOKEN_TYPE, 2, "EOF")]),
        ("345", [Token(NUM_TOKEN_TYPE, 2, "345"), Token(EOF_TOKEN_TYPE, 3, "EOF")])
        ])
    def test_lex_multi_digit_number(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()


    @pytest.mark.parametrize("program,token_list", [
        ("1 + 2", [Token(NUM_TOKEN_TYPE, 0, "1"), Token(PLUS_TOKEN_TYPE, 2, "+"), Token(NUM_TOKEN_TYPE, 4, "2"), Token(EOF_TOKEN_TYPE, 5, "EOF")]),
        ("3 + 4", [Token(NUM_TOKEN_TYPE, 0, "3"), Token(PLUS_TOKEN_TYPE, 2, "+"), Token(NUM_TOKEN_TYPE, 4, "4"), Token(EOF_TOKEN_TYPE, 5, "EOF")])
        ])
    def test_lex_simple_add(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()


    @pytest.mark.parametrize("program,token_list", [
        ("1 - 2", [Token(NUM_TOKEN_TYPE, 0, "1"), Token(MINUS_TOKEN_TYPE, 2, "-"), Token(NUM_TOKEN_TYPE, 4, "2"), Token(EOF_TOKEN_TYPE, 5, "EOF")]),
        ("3 - 4", [Token(NUM_TOKEN_TYPE, 0, "3"), Token(MINUS_TOKEN_TYPE, 2, "-"), Token(NUM_TOKEN_TYPE, 4, "4"), Token(EOF_TOKEN_TYPE, 5, "EOF")])
        ])
    def test_lex_simple_subtract(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()


    @pytest.mark.parametrize("program,token_list", [
        ("1 + 2 - 3", [Token(NUM_TOKEN_TYPE, 0, "1"), Token(PLUS_TOKEN_TYPE, 2, "+"), Token(NUM_TOKEN_TYPE, 4, "2"), Token(MINUS_TOKEN_TYPE, 6, "-"), Token(NUM_TOKEN_TYPE, 8, "3"), Token(EOF_TOKEN_TYPE, 9, "EOF")]),
        ("3 - 4 + 5", [Token(NUM_TOKEN_TYPE, 0, "3"), Token(MINUS_TOKEN_TYPE, 2, "-"), Token(NUM_TOKEN_TYPE, 4, "4"), Token(PLUS_TOKEN_TYPE, 6, "+"), Token(NUM_TOKEN_TYPE, 8, "5"), Token(EOF_TOKEN_TYPE, 9, "EOF")])
        ])
    def test_lex_combined_addition_and_subtraction(self, program, token_list):
        lexer = Lexer(program)
        assert token_list == lexer.lex()

class TestLexerBadFormat:
    """
    Testing the lexer with programs that are poorly formatted, like extra spaces.
    """
    def test_lex_extra_spaces(self):
        program = "     1 -      2      "
        token_list = [Token(NUM_TOKEN_TYPE, 5, "1"), Token(MINUS_TOKEN_TYPE, 7, "-"), Token(NUM_TOKEN_TYPE, 14, "2"), Token(EOF_TOKEN_TYPE, 21, "EOF")]
        lexer = Lexer(program)
        assert token_list == lexer.lex()
