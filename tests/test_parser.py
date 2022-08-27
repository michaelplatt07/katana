import pytest

from katana.katana import NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE, LiteralNode, PlusMinusNode, Parser, Token, EOF_TOKEN_TYPE

class TestParserLiterals:

    def test_parser_single_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1"), Token(EOF_TOKEN_TYPE, 1, "EOF")]
        ast = LiteralNode(token_list[0], "1")
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_multi_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, "123"), Token(EOF_TOKEN_TYPE, 1, "EOF")]
        ast = LiteralNode(token_list[0], "123")
        parser = Parser(token_list)
        assert ast == parser.parse()    

class TestParserAddition:

    def test_parser_adding_two_numbers(self):
        """
        Given the simple program:
        1 + 2
        Epxected to return an AST like:
        (1+2)
        """
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1"), Token(PLUS_TOKEN_TYPE, 1, "+"), Token(NUM_TOKEN_TYPE, 2, "2"), Token(EOF_TOKEN_TYPE, 3, "EOF")]
        left_node = LiteralNode(token_list[0], "1")
        right_node = LiteralNode(token_list[2], "2")
        ast = PlusMinusNode(token_list[1], "+", left_node, right_node)
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_adding_three_numbers(self):
        """
        Given the simple program:
        1 + 2 + 3
        Expected to return an AST like:
        ((1+2)+3)
        """
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1"), Token(PLUS_TOKEN_TYPE, 1, "+"), Token(NUM_TOKEN_TYPE, 2, "2"), Token(PLUS_TOKEN_TYPE, 3, "+"), Token(NUM_TOKEN_TYPE, 4, "3"), Token(EOF_TOKEN_TYPE, 5, "EOF")]
        left_node_1 = LiteralNode(token_list[0], "1")
        right_node_1 = LiteralNode(token_list[2], "2")
        first_plus = PlusMinusNode(token_list[1], "+", left_node_1, right_node_1)
        right_node_2 = LiteralNode(token_list[4], "3")
        ast = PlusMinusNode(token_list[3], "+", first_plus, right_node_2)
        parser = Parser(token_list)
        assert ast == parser.parse()

class TestParserSubtraction:

    def test_parser_adding_subtracting_numbers(self):
        """
        Given the simple program:
        1 - 2
        Epxected to return an AST like:
        (1-2)
        """
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1"), Token(MINUS_TOKEN_TYPE, 1, "-"), Token(NUM_TOKEN_TYPE, 2, "2"), Token(EOF_TOKEN_TYPE, 3, "EOF")]
        left_node = LiteralNode(token_list[0], "1")
        right_node = LiteralNode(token_list[2], "2")
        ast = PlusMinusNode(token_list[1], "-", left_node, right_node)
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_subtracting_three_numbers(self):
        """
        Given the simple program:
        1 - 2 - 3
        Expected to return an AST like:
        ((1-2)-3)
        """
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1"), Token(MINUS_TOKEN_TYPE, 1, "-"), Token(NUM_TOKEN_TYPE, 2, "2"), Token(MINUS_TOKEN_TYPE, 3, "-"), Token(NUM_TOKEN_TYPE, 4, "3"), Token(EOF_TOKEN_TYPE, 5, "EOF")]
        left_node_1 = LiteralNode(token_list[0], "1")
        right_node_1 = LiteralNode(token_list[2], "2")
        first_plus = PlusMinusNode(token_list[1], "-", left_node_1, right_node_1)
        right_node_2 = LiteralNode(token_list[4], "3")
        ast = PlusMinusNode(token_list[3], "-", first_plus, right_node_2)
        parser = Parser(token_list)
        assert ast == parser.parse()


