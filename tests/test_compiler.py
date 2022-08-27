import pytest
from katana.katana import MINUS_TOKEN_TYPE, NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE, Lexer, LiteralNode, PlusMinusNode, Parser, Token


class TestCompiler:

    def test_simple_math_program(self):
        """
        Given a simple mathmatics program like:
        1 + 2 + 3 - 4
        Expected result of:
        (((1+2)+3)-4)
        """
        lexer = Lexer("1 + 2 + 3 - 4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1"), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2"), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3"), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 12, "4"), "4")
        plus_token_one = PlusMinusNode(Token(PLUS_TOKEN_TYPE, 2, "+"), "+", literal_one, literal_two)
        plus_token_two = PlusMinusNode(Token(PLUS_TOKEN_TYPE, 6, "+"), "+", plus_token_one, literal_three)
        minus_token_one = PlusMinusNode(Token(MINUS_TOKEN_TYPE, 10, "-"), "-",  plus_token_two, literal_four)
        expected_ast = minus_token_one
        assert expected_ast == parser.parse()

    def test_simple_math_program_bad_format(self):
        """
        Given a simple mathmatics program with extra spaces like:
        1 +      2  +     3 -      4
        Expected result of:
        (((1+2)+3)-4)
        """
        lexer = Lexer("1 +      2  +     3 -      4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1"), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 9, "2"), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 18, "3"), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 27, "4"), "4")
        plus_token_one = PlusMinusNode(Token(PLUS_TOKEN_TYPE, 2, "+"), "+", literal_one, literal_two)
        plus_token_two = PlusMinusNode(Token(PLUS_TOKEN_TYPE, 12, "+"), "+", plus_token_one, literal_three)
        minus_token_one = PlusMinusNode(Token(MINUS_TOKEN_TYPE, 20, "-"), "-",  plus_token_two, literal_four)
        expected_ast = minus_token_one
        assert expected_ast == parser.parse()


