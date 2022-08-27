import pytest

from katana.katana import MINUS_TOKEN_TYPE, NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE, Lexer, Token, EOF_TOKEN_TYPE

class TestLexer:

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
