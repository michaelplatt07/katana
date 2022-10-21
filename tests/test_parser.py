import pytest

from katana.katana import (
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    LiteralNode,
    MINUS_TOKEN_TYPE,
    MultiplyDivideNode,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    Parser,
    PlusMinusNode,
    Token,
    HIGH,
    MEDIUM,
    LOW
)


class TestParserLiterals:

    def test_parser_single_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, "1", LOW),
                      Token(EOF_TOKEN_TYPE, 1, "EOF", LOW)]
        ast = LiteralNode(token_list[0], "1")
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_multi_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, "123", LOW),
                      Token(EOF_TOKEN_TYPE, 1, "EOF", LOW)]
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
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "2", LOW),
            Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
        ]
        left_node = LiteralNode(token_list[0], "1")
        right_node = LiteralNode(token_list[2], "2")
        ast = PlusMinusNode(token_list[1], "+", left_node, right_node)
        left_node.parent_node = ast
        right_node.parent_node = ast
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_adding_three_numbers(self):
        """
        Given the simple program:
        1 + 2 + 3
        Expected to return an AST like:
        ((1+2)+3)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 6, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, "3", LOW),
            Token(EOF_TOKEN_TYPE, 9, "EOF", LOW),
        ]
        left_node_1 = LiteralNode(token_list[0], "1")
        right_node_1 = LiteralNode(token_list[2], "2")
        first_plus = PlusMinusNode(
            token_list[1], "+", left_node_1, right_node_1)
        right_node_2 = LiteralNode(token_list[4], "3")
        ast = PlusMinusNode(token_list[3], "+", first_plus, right_node_2)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestParserSubtraction:
    def test_parser_two_subtracting_numbers(self):
        """
        Given the simple program:
        1 - 2
        Epxected to return an AST like:
        (1-2)
        """

        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "2", LOW),
            Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
        ]
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

        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, "2", LOW),
            Token(MINUS_TOKEN_TYPE, 6, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, "3", LOW),
            Token(EOF_TOKEN_TYPE, 9, "EOF", LOW),
        ]
        left_node_1 = LiteralNode(token_list[0], "1")
        right_node_1 = LiteralNode(token_list[2], "2")
        first_plus = PlusMinusNode(
            token_list[1], "-", left_node_1, right_node_1)
        right_node_2 = LiteralNode(token_list[4], "3")
        ast = PlusMinusNode(token_list[3], "-", first_plus, right_node_2)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestMultiply:
    def test_parser_multiply_two_numbers(self):
        """
        Given a simple program like:
        3 * 4
        Expected to return an AST like:
        (3*4)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, "4", LOW),
            Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
        ]
        left_node = LiteralNode(token_list[0], "3")
        right_node = LiteralNode(token_list[2], "4")
        ast = MultiplyDivideNode(token_list[1], "*", left_node, right_node)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestDivide:
    def test_parser_divide_two_numbers(self):
        """
        Given a simple program like:
        3 / 4
        Expected to return an AST like:
        (3/4)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "3", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, "4", LOW),
            Token(EOF_TOKEN_TYPE, 5, "EOF", LOW),
        ]
        left_node = LiteralNode(token_list[0], "3")
        right_node = LiteralNode(token_list[2], "4")
        ast = MultiplyDivideNode(token_list[1], "/", left_node, right_node)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestComments:
    def test_parser_simple_add_with_comment(self):
        """
        Given a simple program like:
        3 + 4 // Add numbers
        Expected to return an AST like:
        (3/4)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 2, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, "4", LOW),
            Token(COMMENT_TOKEN_TYPE, 6, "4", LOW),
            Token(EOF_TOKEN_TYPE, 21, "EOF", LOW),
        ]
        left_node = LiteralNode(token_list[0], "3")
        right_node = LiteralNode(token_list[2], "4")
        ast = PlusMinusNode(token_list[1], "/", left_node, right_node)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestArithmetic:
    def test_parser_add_and_multiply(self):
        """
        Given a program like:
        2 + 3 * 4
        Expected to return an AST like:
        (2+(3*4))
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, "4", LOW),
            Token(EOF_TOKEN_TYPE, 10, "EOF", LOW),
        ]
        left_node_add = LiteralNode(token_list[0], "2")
        left_node_multiply = LiteralNode(token_list[2], "3")
        right_node_multiply = LiteralNode(token_list[4], "4")
        multiply_node = MultiplyDivideNode(
            token_list[3], "*", left_node_multiply, right_node_multiply)
        add_node = PlusMinusNode(
            token_list[1], "+", left_node_add, multiply_node)
        ast = add_node
        parser = Parser(token_list)
        assert ast == parser.parse()

    @pytest.mark.skip
    def test_parser_add_and_multiply_more_complex(self):
        """
        Given a program like:
        2 + 3 * 4 + 5
        Expected to return an AST like:
        ((2+(3*4))+5)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, "4", LOW),
            Token(EOF_TOKEN_TYPE, 10, "EOF", LOW),
        ]
        left_node_add = LiteralNode(token_list[0], "2")
        left_node_multiply = LiteralNode(token_list[2], "3")
        right_node_multiply = LiteralNode(token_list[4], "4")
        multiply_node = MultiplyDivideNode(
            token_list[3], "*", left_node_multiply, right_node_multiply)
        add_node = PlusMinusNode(
            token_list[1], "+", left_node_add, multiply_node)
        ast = add_node
        parser = Parser(token_list)
        assert ast == parser.parse()
