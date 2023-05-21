import pytest
import re
from unittest.mock import patch

from katana.katana import (
    AssignmentNode,
    BooleanNode,
    CharNode,
    CompareNode,
    FunctionKeywordNode,
    NumberNode,
    LogicKeywordNode,
    LoopDownKeywordNode,
    LoopFromKeywordNode,
    LoopUpKeywordNode,
    MultiplyDivideNode,
    Parser,
    PlusMinusNode,
    RangeNode,
    StartNode,
    StringNode,
    VariableNode,
    VariableKeywordNode,
    VariableReferenceNode,
    BufferOverflowException,
    KeywordMisuseException,
    InvalidArgsException,
    InvalidAssignmentException,
    InvalidConcatenationException,
    InvalidTypeDeclarationException,
    NotEnoughArgsException,
    TooManyArgsException,
    Token,
    ASSIGNMENT_TOKEN_TYPE,
    BOOLEAN_TOKEN_TYPE,
    CHARACTER_TOKEN_TYPE,
    COMMA_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EQUAL_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    LESS_THAN_TOKEN_TYPE,
    GREATER_THAN_TOKEN_TYPE,
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
    CHAR_AT_SIGNATURE,
    COPY_STR_SIGNATURE,
    LOOP_DOWN_SIGNATURE,
    LOOP_FROM_SIGNATURE,
    LOOP_UP_SIGNATURE,
    MAIN_SIGNATURE,
    PRINT_SIGNATURE,
    UPDATE_CHAR_SIGNATURE,
)


class TestParserLiterals:

    def test_parser_single_digit_literal(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 1, 0, "1", LOW),
            Token(EOL_TOKEN_TYPE, 2, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 3, 0, "EOF", LOW)
        ]
        one_node = NumberNode(token_list[4], "1")
        ast = StartNode(token_list[0], "main", [one_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_multi_digit_literal(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "123", LOW),
            Token(EOL_TOKEN_TYPE, 3, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        num_node = NumberNode(token_list[4], "123")
        ast = StartNode(token_list[0], "main", [num_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserAddition:
    """
    Tests for snippets for addition.
    """

    def test_parser_adding_two_numbers(self):
        """
        Given the simple program:
        main() {
            1 + 2;
        }
        Epxected to return an AST like:
        (1+2)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        left_node = NumberNode(token_list[4], "1")
        right_node = NumberNode(token_list[6], "2")
        plus_minus_node = PlusMinusNode(token_list[5], "+", left_node, right_node)
        ast = StartNode(token_list[0], "main", [plus_minus_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_adding_three_numbers(self):
        """
        Given the simple program:
        main() {
            1 + 2 + 3;
        }
        Expected to return an AST like:
        ((1+2)+3)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 6, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 9, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        left_node_1 = NumberNode(token_list[4], "1")
        right_node_1 = NumberNode(token_list[6], "2")
        first_plus = PlusMinusNode(
            token_list[5], "+", left_node_1, right_node_1)
        right_node_2 = NumberNode(token_list[8], "3")
        second_plus = PlusMinusNode(token_list[7], "+", first_plus, right_node_2)
        ast = StartNode(token_list[0], "main", [second_plus])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserSubtraction:
    """
    Tests for parsing subtraction snippets.
    """

    def test_parser_two_subtracting_numbers(self):
        """
        Given the simple program:
        main() {
            1 - 2;
        }
        Epxected to return an AST like:
        (1-2)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        left_node = NumberNode(token_list[4], "1")
        right_node = NumberNode(token_list[6], "2")
        plus_minus_node = PlusMinusNode(token_list[5], "-", left_node, right_node)
        ast = StartNode(token_list[0], "main", [plus_minus_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_subtracting_three_numbers(self):
        """
        Given the simple program:
        main() {
            1 - 2 - 3;
        }
        Expected to return an AST like:
        ((1-2)-3)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 9, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        left_node_1 = NumberNode(token_list[4], "1")
        right_node_1 = NumberNode(token_list[6], "2")
        first_minus = PlusMinusNode(
            token_list[5], "-", left_node_1, right_node_1)
        right_node_2 = NumberNode(token_list[8], "3")
        second_minus = PlusMinusNode(token_list[7], "-", first_minus, right_node_2)
        ast = StartNode(token_list[0], "main", [second_minus])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestMultiply:
    """
    Tests for snippets for multiplication.
    """

    def test_parser_multiply_two_numbers(self):
        """
        Given a simple program like:
        main() {
            3 * 4
        }
        Expected to return an AST like:
        (3*4)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        left_node = NumberNode(token_list[4], "3")
        right_node = NumberNode(token_list[6], "4")
        mult_div_node = MultiplyDivideNode(token_list[5], "*", left_node, right_node)
        ast = StartNode(token_list[0], "main", [mult_div_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestDivide:
    """
    Tests for snippets for division.
    """

    def test_parser_divide_two_numbers(self):
        """
        Given a simple program like:
        main() {
            3 / 4
        }
        Expected to return an AST like:
        (3/4)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, 1, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        left_node = NumberNode(token_list[4], "3")
        right_node = NumberNode(token_list[6], "4")
        mult_div_node = MultiplyDivideNode(token_list[5], "/", left_node, right_node)
        ast = StartNode(token_list[0], "main", [mult_div_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestComments:
    """
    All tests related to parsing out comments.
    """

    def test_parser_simple_add_with_comment(self):
        """
        Given a simple program like:
        main() {
            3 + 4; // Add numbers
        }
        Expected to return an AST like:
        (3+4)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(EOL_TOKEN_TYPE, 5, 1, ";", LOW),
            Token(COMMENT_TOKEN_TYPE, 8, 1, "// Add numbers", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        left_node = NumberNode(token_list[4], "3")
        right_node = NumberNode(token_list[6], "4")
        plus_minus_node = PlusMinusNode(token_list[5], "+", left_node, right_node)
        ast = StartNode(token_list[0], "main", [plus_minus_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestArithmetic:
    """
    Tests for order of operations for mathematics.
    """

    def test_parser_add_and_multiply(self):
        """
        Given a program like:
        main() {
            2 + 3 * 4
        }
        Expected to return an AST like:
        (2+(3*4))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(EOL_TOKEN_TYPE, 9, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        left_node_add = NumberNode(token_list[4], "2")
        left_node_multiply = NumberNode(token_list[6], "3")
        right_node_multiply = NumberNode(token_list[8], "4")
        multiply_node = MultiplyDivideNode(
            token_list[7], "*", left_node_multiply, right_node_multiply)
        add_node = PlusMinusNode(
            token_list[5], "+", left_node_add, multiply_node)
        ast = StartNode(token_list[0], "main", [add_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_multiply_sub_add_more_complex(self):
        """
        Given a program like:
        main() {
            2 * 3 - 4 + 5;
        }
        Expected to return an AST like:
        (((2*3)-4)+5)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(PLUS_TOKEN_TYPE, 10, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW),
        ]
        two_node = NumberNode(token_list[4], "2")
        three_node = NumberNode(token_list[6], "3")
        four_node = NumberNode(token_list[8], "4")
        five_node = NumberNode(token_list[10], "5")
        multiply_node = MultiplyDivideNode(
            token_list[5], "*", two_node, three_node)
        sub_node = PlusMinusNode(token_list[7], "-", multiply_node, four_node)
        plus_node = PlusMinusNode(token_list[9], "+", sub_node, five_node)
        ast = StartNode(token_list[0], "main", [plus_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_add_sub_and_multiply_more_complex(self):
        """
        Given a program like:
        main() {
            2 + 3 - 4 * 5
        }
        Expected to return an AST like:
        ((2+3)-(4*5))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW),
        ]
        two_node = NumberNode(token_list[4], "2")
        three_node = NumberNode(token_list[6], "3")
        four_node = NumberNode(token_list[8], "4")
        five_node = NumberNode(token_list[10], "5")
        multiply_node = MultiplyDivideNode(
            token_list[9], "*", four_node, five_node)
        plus_node = PlusMinusNode(token_list[5], "+", two_node, three_node)
        sub_node = PlusMinusNode(token_list[7], "-", plus_node, multiply_node)
        ast = StartNode(token_list[0], "main", [sub_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_add_multiply_sub_more_complex(self):
        """
        Given a program like:
        main() {
            2 + 3 * 4 - 5
        }
        Expected to return an AST like:
        ((2+(3*4))-5)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(MINUS_TOKEN_TYPE, 10, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        two_node = NumberNode(token_list[4], "2")
        three_node = NumberNode(token_list[6], "3")
        four_node = NumberNode(token_list[8], "4")
        five_node = NumberNode(token_list[10], "5")
        multiply_node = MultiplyDivideNode(
            token_list[7], "*", three_node, four_node)
        plus_node = PlusMinusNode(token_list[5], "+", two_node, multiply_node)
        sub_node = PlusMinusNode(token_list[9], "-", plus_node, five_node)
        ast = StartNode(token_list[0], "main", [sub_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_parser_div_add_mul_more_complex(self):
        """
        Given a program like:
        main() {
            8 / 8 + 3 * 2
        }
        Expected to return an AST like:
        ((8*8)+(3*2))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "8", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, 1, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "8", LOW),
            Token(PLUS_TOKEN_TYPE, 6, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, 2, "2", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        first_eight_node = NumberNode(token_list[4], "8")
        second_eight_node = NumberNode(token_list[6], "8")
        three_node = NumberNode(token_list[8], "3")
        two_node = NumberNode(token_list[10], "2")
        divide_node = MultiplyDivideNode(
            token_list[5], "/", first_eight_node, second_eight_node)
        multiply_node = MultiplyDivideNode(
            token_list[9], "*", three_node, two_node)
        add_node = PlusMinusNode(
            token_list[7], "+", divide_node, multiply_node)
        ast = StartNode(token_list[0], "main", [add_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserParenthesis:
    """
    Testing that parenethesis work as expected such as for order of operations.
    """

    def test_simple_add_with_paren(self):
        """
        Given a program like:
        main(){
            1 + (2 + 3);
        }
        Expected to return an AST like:
        (1+(2+3))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 7, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 9, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        one_node = NumberNode(token_list[4], "1")
        two_node = NumberNode(token_list[7], "2")
        three_node = NumberNode(token_list[9], "3")
        first_plus = PlusMinusNode(
            token_list[8], "+", two_node, three_node)
        other_plus = PlusMinusNode(token_list[5], "+", one_node, first_plus)
        ast = StartNode(token_list[0], "main", [other_plus])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_add_higher_prio_than_mult_with_paren(self):
        """
        Given a program like:
        main() {
            (1 + 2) * 3)
        }
        Expected to return an AST like:
        ((1+2)*3)
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 1, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 3, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 1, ")", VERY_HIGH),
            Token(MULTIPLY_TOKEN_TYPE, 8, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        one_node = NumberNode(token_list[5], "1")
        two_node = NumberNode(token_list[7], "2")
        three_node = NumberNode(token_list[10], "3")
        first_plus = PlusMinusNode(
            token_list[6], "+", one_node, two_node)
        mult_node = MultiplyDivideNode(token_list[9], "*", first_plus, three_node)
        ast = StartNode(token_list[0], "main", [mult_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserPrint:
    """
    All tests related to the print keyword.
    """

    def test_keyword_print_with_literal(self):
        """
        Given a program like:
        main() {
            print(3);
        }
        Expected to return an AST like:
        (print(3))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 1, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 6, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 1, ")", HIGH),
            Token(EOL_TOKEN_TYPE, 8, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        three_node = NumberNode(token_list[6], "3")
        print_node = FunctionKeywordNode(token_list[4], "print", [three_node])
        ast = StartNode(token_list[0], "main", [print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_keyword_printl(self):
        """
        Given a program like:
        main() {
            printl(3);
        }
        Expected to return an AST like:
        (main[(printl(3))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "printl", 5),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 5),
            Token(NUM_TOKEN_TYPE, 11, 1, "3", 1),
            Token(RIGHT_PAREN_TOKEN_TYPE, 12, 1, ")", 5),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        three_node = NumberNode(token_list[6], "3")
        printl_node = FunctionKeywordNode(token_list[4], "printl", [three_node])
        ast = StartNode(token_list[0], "main", [printl_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_print_use_invalid(self, mock_print):
        """
        Given a progrma like:
        main() {
            print();
        }
        Expected KeywordMisuseException to be raised
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 9, 1, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(1, 4, 'print', PRINT_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_print_no_left_paren_raises_error(self, mock_print):
        """
        Given a progrma like:
        main() {
            print{1);
        }
        Expected KeywordMisuseException to be raised
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "print", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 9, 1, "{", 3),
            Token(NUM_TOKEN_TYPE, 10, 1, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 12, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(1, 4, 'print', PRINT_SIGNATURE))


class TestParserMain:
    """
    All tests related to the main keyword.
    """

    def test_keyword_main_with_literal(self):
        """
        Given a program like:
        main() { 3; };
        Expected to return an AST like:
        (main(3))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 12, 0, "}", HIGH),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        three_node = NumberNode(token_list[4], "3")
        ast = StartNode(token_list[0], "main", [three_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_main_with_no_left_paren_raises_exception(self, mock_print):
        """
        Given a program like:
        main{1) { 3; };
        Expected to raise an error.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 4, 0, "{", HIGH),
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 0, ")", HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 8, 0, "{", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 12, 0, "}", HIGH),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 0, KeywordMisuseException(0, 0, "main", MAIN_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_main_with_method_params_raises_exception(self, mock_print):
        """
        Given a program like:
        main(1) { 3; };
        Expected to raise an error.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 0, ")", HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 8, 0, "{", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 12, 0, "}", HIGH),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 0, KeywordMisuseException(0, 0, "main", MAIN_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_main_with_no_right_paren_raises_exception(self, mock_print):
        """
        Given a program like:
        main(1} { 3; };
        Expected to raise an error.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 0, "}", HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 8, 0, "{", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 12, 0, "}", HIGH),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 0, KeywordMisuseException(0, 0, "main", MAIN_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_main_with_no_left_curl_brace_raises_exception(self, mock_print):
        """
        Given a program like:
        main(1) ( 3; };
        Expected to raise an error.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 5, 0, "1", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 0, ")", HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 8, 0, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 9, 0, "3", LOW),
            Token(EOL_TOKEN_TYPE, 10, 0, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 12, 0, "}", HIGH),
            Token(EOL_TOKEN_TYPE, 13, 0, ";", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 0, KeywordMisuseException(0, 0, "main", MAIN_SIGNATURE))


class TestParserInt:
    """
    All tests related to the int keyword.
    """

    def test_keyword_int_64_declaration_from_expression(self):
        """
        Given a program like:
        main() {
            int64 x = 3 + 4;
        }
        Expected to return an AST like:
        (main[(int64((x=(3+4))))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 12, 1, "+", HIGH),
            Token(NUM_TOKEN_TYPE, 14, 1, "4", LOW),
            Token(EOL_TOKEN_TYPE, 15, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        three_node = NumberNode(token_list[7], "3")
        four_node = NumberNode(token_list[9], "4")
        plus_node = PlusMinusNode(token_list[8], "+", three_node, four_node)
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, plus_node)
        keyword_node = VariableKeywordNode(token_list[4], "int64", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_keyword_int_64_declaration(self):
        """
        Given a program like:
        main() {
            int64 x = 3;
        }
        Expected to return an AST like:
        (main[(int64((x=3)))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        three_node = NumberNode(token_list[7], "3")
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, three_node)
        keyword_node = VariableKeywordNode(token_list[4], "int64", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_keyword_const_with_int(self):
        """
        main() {
            const int64 x = 3;
        }
        Expected to return an AST like:
        (main[(const(int64((x=3))))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "const", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 6, "int64", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 12, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 14, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 16, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 17, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        three_node = NumberNode(token_list[8], "3")
        x_node = VariableNode(token_list[6], "x", True)
        assignment_node = AssignmentNode(token_list[7], "=", x_node, three_node)
        variable_dec_node = VariableKeywordNode(token_list[5], "int64", assignment_node)
        const_node = VariableKeywordNode(token_list[4], "const", variable_dec_node)
        ast = StartNode(token_list[0], "main", [const_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_keyword_int_64_reference(self):
        """
        Given a program like:
        main() {
            int64 x = 3;
            print(x);
        }
        Expected to return an AST like:
        (main[(int64((x=3))), (print(x))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
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
        three_node = NumberNode(token_list[7], "3")
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, three_node)
        variable_dec_node = VariableKeywordNode(token_list[4], "int64", assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        print_node = FunctionKeywordNode(token_list[9], "print", [x_ref_node])
        ast = StartNode(token_list[0], "main", [variable_dec_node, print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_int_8_variable_declaration_overflow(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "int8", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(NUM_TOKEN_TYPE, 13, 1, "288", 0),
            Token(EOL_TOKEN_TYPE, 16, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, BufferOverflowException(1, 4))

    @patch("katana.katana.print_exception_message")
    def test_int_16_variable_declaration_overflow(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "int16", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 1, "65538", 0),
            Token(EOL_TOKEN_TYPE, 19, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, BufferOverflowException(1, 4))

    @patch("katana.katana.print_exception_message")
    def test_int_32_variable_declaration_overflow(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "int32", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 1, "4294967298", 0),
            Token(EOL_TOKEN_TYPE, 24, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, BufferOverflowException(1, 4))



class TestParserCharAt:
    """
    All tests related to the charAt keyword.
    """

    def test_char_at_keyword(self):
        """
        Given a program like:
        main() {
            string x = "Hello, Katana!";
            char y = charAt(x, 2);
            if (y == 'l') {
                print("equal");
            } else {
                print("unequal");
            }
        }
        Expected to return an AST like:
        (main[(string(x="Hello, Katana!")), (char(y=(charAt(x,2)))), (if(y='l'), [(print("equal"))], [(print("unequal"))])])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 11, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 13, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 15, "Hello, Katana!", 0),
            Token(EOL_TOKEN_TYPE, 1, 31, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 2, 9, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 11, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 2, 13, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 19, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 20, "x", 0),
            Token(COMMA_TOKEN_TYPE, 2, 21, ",", 0),
            Token(NUM_TOKEN_TYPE, 2, 23, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 24, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 25, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 7, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 8, "y", 0),
            Token(EQUAL_TOKEN_TYPE, 3, 10, "==", 2),
            Token(CHARACTER_TOKEN_TYPE, 3, 14, "l", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 16, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 3, 18, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 14, "equal", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 22, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 5, 11, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 6, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 6, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 6, 14, "unequal", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 6, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 8, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 9, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[7], "Hello, Katana!")
        x_node = VariableNode(token_list[5], "x", False)
        x_assign_node = AssignmentNode(token_list[6], "=", x_node, string_node)
        string_declare_node = VariableKeywordNode(token_list[4], "string", x_assign_node)
        two_node = NumberNode(token_list[16], "2")
        x_ref_node = VariableReferenceNode(token_list[14], "x")
        char_at_node = FunctionKeywordNode(token_list[12], "charAt", [x_ref_node, two_node])
        y_node = VariableNode(token_list[10], "y", False)
        y_assign_node = AssignmentNode(token_list[11], "=", y_node, char_at_node)
        char_declare_node = VariableKeywordNode(token_list[9], "char", y_assign_node)
        char_l_node = CharNode(token_list[23], "l")
        y_ref_node = VariableReferenceNode(token_list[21], "y")
        compare_node = CompareNode(token_list[22], "==", y_ref_node, char_l_node)
        equal_string_node = StringNode(token_list[28], "equal")
        unequal_string_node = StringNode(token_list[36], "unequal")
        print_equal_node = FunctionKeywordNode(token_list[26], "print", [equal_string_node])
        print_unequal_node = FunctionKeywordNode(token_list[34], "print", [unequal_string_node])
        conditional_node = LogicKeywordNode(token_list[19], "if", compare_node, true_side=[print_equal_node], false_side=[print_unequal_node])
        ast = StartNode(token_list[0], "main", [string_declare_node, char_declare_node, conditional_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_char_at_invalid_syntax(self, mock_print):
        """
        Given a program like:
        main() {
            char x = charAt();
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 1, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 1, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 20, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 21, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, KeywordMisuseException(1, 13, "charAt", CHAR_AT_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_char_at_no_left_paren_raises_error(self, mock_print):
        """
        Given a program like:
        main() {
            char x = charAt{);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 1, "charAt", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 19, 1, "{", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 20, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 21, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, KeywordMisuseException(1, 13, "charAt", CHAR_AT_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_char_at_not_enough_params_raises_error(self, mock_print):
        """
        Given a program like:
        main() {
            char x = charAt(3);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 1, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 20, 1, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 21, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, NotEnoughArgsException(1, 13))

    @patch("katana.katana.print_exception_message")
    def test_char_at_invalid_type_first_param(self, mock_print):
        """
        Given a program like:
        main() {
            char x = charAt(12, 2);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 1, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 20, 1, "12", 0),
            Token(COMMA_TOKEN_TYPE, 22, 1, ",", 0),
            Token(NUM_TOKEN_TYPE, 24, 1, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 25, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 26, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, InvalidArgsException(1, 13, "charAt", NumberNode))

    @patch("katana.katana.print_exception_message")
    def test_char_at_invalid_type_second_param(self, mock_print):
        """
        Given a program like:
        main() {
            char x = charAt("hello", 'x');
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 1, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 1, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 1, "(", 3),
            Token(STRING_TOKEN_TYPE, 21, 1, "hello", 0),
            Token(COMMA_TOKEN_TYPE, 27, 1, ",", 0),
            Token(CHARACTER_TOKEN_TYPE, 30, 1, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 32, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 33, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, InvalidArgsException(1, 13, "charAt", CharNode))

    @patch("katana.katana.print_exception_message")
    def test_char_at_invalid_type_first_param_as_var(self, mock_print):
        """
        Given a program like:
        main() {
            int64 y = 12;
            char x = charAt(y, 2);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 1, "12", 0),
            Token(EOL_TOKEN_TYPE, 16, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 2, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 2, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 2, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 2, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 20, 2, "y", 0),
            Token(COMMA_TOKEN_TYPE, 21, 2, ",", 0),
            Token(NUM_TOKEN_TYPE, 23, 2, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 24, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 25, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, InvalidArgsException(2, 13, "charAt", "int64"))

    @patch("katana.katana.print_exception_message")
    def test_char_at_invalid_type_second_param_as_var(self, mock_print):
        """
        Given a program like:
        main() {
            char y = 'z';
            char x = charAt("hello", y);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(CHARACTER_TOKEN_TYPE, 15, 1, "z", 0),
            Token(EOL_TOKEN_TYPE, 17, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 9, 2, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 11, 2, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 13, 2, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 19, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 21, 2, "hello", 0),
            Token(COMMA_TOKEN_TYPE, 27, 2, ",", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 29, 2, "y", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 30, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 31, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 13, InvalidArgsException(2, 13, "charAt", "char"))


class TestUpdateChar:
    """
    All tests related to the udpateChar method
    """

    def test_update_char_function(self):
        """
        Given a program like:
        main() {
            string x = "Hello";
            updateChar(x, 0, 'Q');
        }
        Expected to return an AST like:
        (main[(string(x="Hello, Katana!")), (updateChar(x,0,'Q'))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 11, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 13, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 15, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 1, 22, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "updateChar", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 14, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 15, "x", 0),
            Token(COMMA_TOKEN_TYPE, 2, 16, ",", 0),
            Token(NUM_TOKEN_TYPE, 2, 18, "0", 0),
            Token(COMMA_TOKEN_TYPE, 2, 19, ",", 0),
            Token(CHARACTER_TOKEN_TYPE, 2, 22, "Q", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 24, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 25, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 4, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[7], "Hello")
        x_node = VariableNode(token_list[5], "x", False)
        x_assign_node = AssignmentNode(token_list[6], "=", x_node, string_node)
        string_declare_node = VariableKeywordNode(token_list[4], "string", x_assign_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        zero_node = NumberNode(token_list[13], "0")
        q_char_node = CharNode(token_list[15], "Q")
        update_char_node = FunctionKeywordNode(token_list[9], "updateChar", [x_ref_node, zero_node, q_char_node])
        ast = StartNode(token_list[0], "main", [string_declare_node, update_char_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_update_char_function_invalid_syntax(self, mock_print):
        """
        Given a program like:
        main() {
            string x = "Hello";
            updateChar();
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 11, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 13, 1, "=", 2),
            Token(STRING_TOKEN_TYPE, 15, 1, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "updateChar", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 14, 2, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 16, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(2, 4, "updateChar", UPDATE_CHAR_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_update_char_function_no_left_paren_raises_error(self, mock_print):
        """
        Given a program like:
        main() {
            string x = "Hello";
            updateChar{);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 11, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 13, 1, "=", 2),
            Token(STRING_TOKEN_TYPE, 15, 1, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "updateChar", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 14, 2, "{", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 16, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(2, 4, "updateChar", UPDATE_CHAR_SIGNATURE))



class TestParserCopyString:
    """
    All tests related to the `copyStr` function.
    """

    def test_copy_str(self):
        """
        Given a program like:
        main() {
            string x = "Hello";
            string y = "Katana";
            copyStr(x, y);
        }
        Expected to return an AST like:
        (main[(string(x="Hello")), (string(y="Katana")), (copyStr(x,y)])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
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
        hello_node = StringNode(token_list[7], "Hello")
        x_node = VariableNode(token_list[5], "x", False)
        x_assign_node = AssignmentNode(token_list[6], "=", x_node, hello_node)
        hello_declare_node = VariableKeywordNode(token_list[4], "string", x_assign_node)
        katana_node = StringNode(token_list[12], "Katana")
        y_node = VariableNode(token_list[10], "y", False)
        y_assign_node = AssignmentNode(token_list[11], "=", y_node, katana_node)
        katana_declare_node = VariableKeywordNode(token_list[9], "string", y_assign_node)
        x_ref_node = VariableReferenceNode(token_list[16], "x")
        y_ref_node = VariableReferenceNode(token_list[18], "y")
        copy_str_node = FunctionKeywordNode(token_list[14], "copyStr", [x_ref_node, y_ref_node])
        ast = StartNode(token_list[0], "main", [hello_declare_node, katana_declare_node, copy_str_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_copy_str_function_invalid_syntax(self, mock_print):
        """
        Given a program like:
        main() {
            string x = "Hello";
            copyStr();
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "copyStr", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 1, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 3, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 1, KeywordMisuseException(0, 1, "copyStr", COPY_STR_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_copy_str_function_no_left_paren_raises_error(self, mock_print):
        """
        Given a program like:
        main() {
            string x = "Hello";
            copyStr{);
        }
        Expected to get a KeywordMisuseException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "copyStr", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "{", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 1, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 3, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 1, KeywordMisuseException(0, 1, "copyStr", COPY_STR_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_copy_str_first_arg_not_string(self, mock_print):
        """
        Given a program like:
        main() {
            copyStr(3, "elloH");
        }
        Expected to get an InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "copyStr", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 11, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 12, 1, "3", 0),
            Token(COMMA_TOKEN_TYPE, 13, 1, ",", 0),
            Token(STRING_TOKEN_TYPE, 16, 1, "elloH", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 23, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 24, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "copyStr", NumberNode))

    @patch("katana.katana.print_exception_message")
    def test_copy_str_second_arg_not_string(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "copyStr", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 11, 1, "(", 3),
            Token(STRING_TOKEN_TYPE, 12, 1, "Hello", 0),
            Token(COMMA_TOKEN_TYPE, 19, 1, ",", 0),
            Token(NUM_TOKEN_TYPE, 21, 1, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 22, 1, ")", 3),
            Token(EOL_TOKEN_TYPE, 23, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "copyStr", NumberNode))

    @patch("katana.katana.print_exception_message")
    def test_copy_str_first_arg_var_not_string(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 11, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 13, 1, "=", 2),
            Token(STRING_TOKEN_TYPE, 15, 1, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 2, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 2, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 2, "3", 0),
            Token(EOL_TOKEN_TYPE, 15, 2, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 3, "copyStr", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 11, 3, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 12, 3, "y", 0),
            Token(COMMA_TOKEN_TYPE, 13, 3, ",", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 15, 3, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 16, 3, ")", 3),
            Token(EOL_TOKEN_TYPE, 17, 3, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0)
                ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(3, 4, "copyStr", "int64"))

    @patch("katana.katana.print_exception_message")
    def test_copy_str_second_arg_var_not_string(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 11, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 13, 1, "=", 2),
            Token(STRING_TOKEN_TYPE, 15, 1, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 2, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 2, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 2, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 2, "3", 0),
            Token(EOL_TOKEN_TYPE, 15, 2, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 3, "copyStr", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 11, 3, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 12, 3, "x", 0),
            Token(COMMA_TOKEN_TYPE, 13, 3, ",", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 15, 3, "y", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 16, 3, ")", 3),
            Token(EOL_TOKEN_TYPE, 17, 3, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0)
                ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(3, 4, "copyStr", "int64"))


class TestParserString:
    """
    All tests related to the string keyword
    """

    def test_keyword_string_declaration(self):
        """
        Given a program like:
        main() {
            string x = "hello";
        }
        Expected to return an AST like:
        (main[(int64((x="hello")))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 12, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        string_node = StringNode(token_list[7], "hello")
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, string_node)
        keyword_node = VariableKeywordNode(token_list[4], "string", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_keyword_string_reference(self):
        """
        Given a program like:
        main() {
            string x = "hello";
            print(x);
        }
        Expected to return an AST like:
        (main[(string((x=3))), (print(x))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 12, 1, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        string_node = StringNode(token_list[7], "hello")
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, string_node)
        variable_dec_node = VariableKeywordNode(token_list[4], "string", assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        print_node = FunctionKeywordNode(token_list[9], "print", [x_ref_node])
        ast = StartNode(token_list[0], "main", [variable_dec_node, print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserChar:
    """
    All tests related to the char keyword.
    """

    def test_keyword_char_declaration(self):
        """
        Given a program like:
        main() {
            char x = 'h';
        }
        Expected to return an AST like:
        (main[(char((x="hello")))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "char", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(CHARACTER_TOKEN_TYPE, 10, 1, "h", LOW),
            Token(EOL_TOKEN_TYPE, 12, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        char_node = CharNode(token_list[7], "h")
        x_node = VariableNode(token_list[5], "x", True)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, char_node)
        keyword_node = VariableKeywordNode(token_list[4], "char", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_update_char_with_invalid_type_fails(self):
        """
        Given a program like:
        main() {
            char x = 'h';
            x = 12;
        }
        Expected to return an AST like:
        (main[(char((x="hello")))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 9, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 11, "=", 2),
            Token(CHARACTER_TOKEN_TYPE, 1, 14, "a", 0),
            Token(EOL_TOKEN_TYPE, 1, 16, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 4, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 6, "=", 2),
            Token(NUM_TOKEN_TYPE, 2, 8, "12", 0),
            Token(EOL_TOKEN_TYPE, 2, 10, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 9, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 10, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 12, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(InvalidAssignmentException, match="9:2 Cannot assign a char with a <class 'katana.katana.NumberNode'>."):
            parser.parse()


class TestParserBool:
    """
    All tests related to the bool keyword.
    """

    def test_keyword_bool_declaration(self):
        """
        Given a program like:
        main() {
            bool x = false;
        }
        Expected to return an AST like:
        (main[(bool((x=false)))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "bool", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(BOOLEAN_TOKEN_TYPE, 9, 1, "false", LOW),
            Token(EOL_TOKEN_TYPE, 14, 1, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        boolean_node = BooleanNode(token_list[7], "false")
        x_node = VariableNode(token_list[5], "x", False)
        assignment_node = AssignmentNode(token_list[6], "=", x_node, boolean_node)
        keyword_node = VariableKeywordNode(token_list[4], "bool", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserIfElse:
    """
    All tests related to the if/else conditionals.
    """

    def test_if_keyword(self):
        """
        Given a program like:
        main() {
            if (1 > 0) {
                print("greater");
            }
            print("lower");
        }
        Expected to return an AST like:
        (main[(if(1>0, print("greater"), None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[19], "lower")
        second_print_node = FunctionKeywordNode(token_list[17], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[13], "greater")
        first_print_node = FunctionKeywordNode(token_list[11], "print", [greater_string_node])
        one_node = NumberNode(token_list[6], "1")
        zero_node = NumberNode(token_list[8], "0")
        greater_than_node = CompareNode(token_list[7], ">", one_node, zero_node)
        if_node = LogicKeywordNode(token_list[4], "if", greater_than_node, None, [first_print_node], [])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_keyword_reversed_compare(self):
        """
        Given a program like:
        main() {
            if (0 > 1) {
                print("greater");
            }
            print("lower");
        }
        Expected to return an AST like:
        (main[(if(1>0, print("greater"), None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "0", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[19], "lower")
        second_print_node = FunctionKeywordNode(token_list[17], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[13], "greater")
        first_print_node = FunctionKeywordNode(token_list[11], "print", [greater_string_node])
        zero_node = NumberNode(token_list[6], "0")
        one_node = NumberNode(token_list[8], "1")
        greater_than_node = CompareNode(token_list[7], ">", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[4], "if", greater_than_node, None, [first_print_node], [])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_else(self):
        """
        Given a program like:
        main() {
            if (0 > 1) {
                print("greater");
                print("greater still");
            } else {
                print("lower");
            }
        }
        Expected to return an AST like:
        (main[(if(1>0, print("greater"), None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "greater still", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 29, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 30, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 4, 11, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 14, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 22, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 8, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[26], "lower")
        second_print_node = FunctionKeywordNode(token_list[24], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[13], "greater")
        first_print_node = FunctionKeywordNode(token_list[11], "print", [greater_string_node])
        greater_still_string_node = StringNode(token_list[18], "greater still")
        second_first_print_node = FunctionKeywordNode(token_list[16], "print", [greater_still_string_node])
        zero_node = NumberNode(token_list[6], "1")
        one_node = NumberNode(token_list[8], "0")
        greater_than_node = CompareNode(token_list[7], ">", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[4], "if", greater_than_node, None, [first_print_node, second_first_print_node], [second_print_node])
        ast = StartNode(token_list[0], "main", [if_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_keyword_less_than_operator(self):
        """
        Given a program like:
        main() {
            if (1 < 0) {
                print("greater");
                print("greater still");
            }
            print("lower");
        }
        Expected to return an AST like:
        (main[(if(1>0, [print("greater"), print("greater still")], None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(LESS_THAN_TOKEN_TYPE, 1, 10, "<", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "greater still", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 29, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 30, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 7, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[24], "lower")
        second_print_node = FunctionKeywordNode(token_list[22], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[13], "greater")
        first_print_node = FunctionKeywordNode(token_list[11], "print", [greater_string_node])
        greater_still_string_node = StringNode(token_list[18], "greater still")
        second_first_print_node = FunctionKeywordNode(token_list[16], "print", [greater_still_string_node])
        zero_node = NumberNode(token_list[6], "1")
        one_node = NumberNode(token_list[8], "0")
        greater_than_node = CompareNode(token_list[7], "<", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[4], "if", greater_than_node, None, [first_print_node, second_first_print_node])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_keyword_equal_operator(self):
        """
        Given a program like:
        main() {
            if (1 == 0) {
                print("greater");
                print("greater still");
            }
            print("lower");
        }
        Expected to return an AST like:
        (main[(if(1==0, [print("greater"), print("greater still")], None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 1, 10, "==", 2),
            Token(NUM_TOKEN_TYPE, 1, 13, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 14, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 16, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "greater still", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 29, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 30, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 7, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[24], "lower")
        second_print_node = FunctionKeywordNode(token_list[22], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[13], "greater")
        first_print_node = FunctionKeywordNode(token_list[11], "print", [greater_string_node])
        greater_still_string_node = StringNode(token_list[18], "greater still")
        second_first_print_node = FunctionKeywordNode(token_list[16], "print", [greater_still_string_node])
        zero_node = NumberNode(token_list[6], "1")
        one_node = NumberNode(token_list[8], "0")
        equal_node = CompareNode(token_list[7], "==", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[4], "if", equal_node, None, [first_print_node, second_first_print_node])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestParserLoopKeyword:
    """
    All tests related to the various loop keywords.
    """

    def test_loop_up_keyword(self):
        """
        Given a program like:
        ```
        main() {
            loopUp(3) {
                print("looping");
            }
        }
        ```
        Expected to return an AST like:
        (main[(loopUp((0<3), [(print("looping"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 10, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 11, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 14, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[11], "looping")
        print_node = FunctionKeywordNode(token_list[9], "print", [string_node])
        three_node = NumberNode(token_list[6], "3")
        loop_node = LoopUpKeywordNode(token_list[4], "loopUp", three_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_loop_up_with_variable_reference(self):
        """
        Given a program like:
        ```
        main() {
            int64 x = 5;
            loopUp(x) {
                print("looping");
            }
        }
        ```
        (main[(int64(x=5))(loopUp((0<x), [(print("looping"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "5", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 10, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 14, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        string_node = StringNode(token_list[16], "looping")
        print_node = FunctionKeywordNode(token_list[14], "print", [string_node])
        five_node = NumberNode(token_list[7], "5")
        x_node = VariableNode(token_list[5], "x", False)
        x_assignment_node = AssignmentNode(token_list[6], "=", x_node, five_node)
        x_int_dec_node = VariableKeywordNode(token_list[4], "int64", x_assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        loop_node = LoopUpKeywordNode(token_list[9], "loopUp", x_ref_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [x_int_dec_node, loop_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_loop_up_with_variable_wrong_type_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            string x = "hello";
            loopUp(x) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 11, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 13, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 15, "hello", 0),
            Token(EOL_TOKEN_TYPE, 1, 22, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 10, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 14, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 2, InvalidArgsException(4, 2, "loopUp", "string"))

    def test_loop_down_keyword(self):
        """
        Given a program like:
        ```
        main() {
            loopDown(3) {
                print("looping");
            }
        }
        ```
        Expected to return an AST like:
        (main[(loopDown((0<3), [(print("looping"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 13, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 14, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 16, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[11], "looping")
        print_node = FunctionKeywordNode(token_list[9], "print", [string_node])
        three_node = NumberNode(token_list[6], "3")
        loop_node = LoopDownKeywordNode(token_list[4], "loopDown", three_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_loop_down_with_variable_reference(self):
        """
        Given a program like:
        ```
        main() {
            int64 x = 7;
            loopDown(x) {
                print("looping");
            }
        }
        ```
        (main[(int64(x=7))(loopDown((x>0), [(print("looping"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "7", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 10, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 14, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        string_node = StringNode(token_list[16], "looping")
        print_node = FunctionKeywordNode(token_list[14], "print", [string_node])
        seven_node = NumberNode(token_list[7], "7")
        x_node = VariableNode(token_list[5], "x", False)
        x_assignment_node = AssignmentNode(token_list[6], "=", x_node, seven_node)
        x_int_dec_node = VariableKeywordNode(token_list[4], "int64", x_assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        loop_node = LoopDownKeywordNode(token_list[9], "loopDown", x_ref_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [x_int_dec_node, loop_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_loop_down_with_variable_wrong_type_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            string x = "hello";
            loopDown(x) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException.
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 11, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 13, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 15, "hello", 0),
            Token(EOL_TOKEN_TYPE, 1, 22, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 10, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 14, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 2, InvalidArgsException(4, 2, "loopDown", "string"))

    def test_loop_from_keyword(self):
        """
        Given a program like:
        ```
        main() {
            loopFrom(0..3) {
                print("looping");
            }
        }
        ```
        Expected to return an AST like:
        (main[(loopFrom((0..3), [(print("looping"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 13, "0", 0),
            Token(RANGE_INDICATION_TOKEN_TYPE, 1, 14, "..", 0),
            Token(NUM_TOKEN_TYPE, 1, 16, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 17, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 18, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[13], "looping")
        print_node = FunctionKeywordNode(token_list[11], "print", [string_node])
        zero_node = NumberNode(token_list[6], "0")
        three_node = NumberNode(token_list[8], "3")
        range_node = RangeNode(token_list[7], "..", zero_node, three_node)
        loop_node = LoopFromKeywordNode(token_list[4], "loopFrom", range_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    @patch("katana.katana.print_exception_message")
    def test_loop_from_keyword_without_dot_operator_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopFrom(0) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 12, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 13, 1, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 14, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 16, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 23, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 24, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "loopFrom", NumberNode))

    @patch("katana.katana.print_exception_message")
    def test_loop_up_with_string_in_params_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopUp("hello") {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", ""),
            Token(RIGHT_PAREN_TOKEN_TYPE, 16, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 18, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "loopUp", StringNode))

    @patch("katana.katana.print_exception_message")
    def test_loop_down_with_string_in_params_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopDown("hello") {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", ""),
            Token(RIGHT_PAREN_TOKEN_TYPE, 16, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 18, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "loopDown", StringNode))

    @patch("katana.katana.print_exception_message")
    def test_loop_up_with_dot_operator_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopUp(0..5) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 11, 1, "0", ""),
            Token(RANGE_INDICATION_TOKEN_TYPE, 12, 1, "..", ""),
            Token(NUM_TOKEN_TYPE, 14, 1, "5", ""),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 17, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "loopUp", RangeNode))

    @patch("katana.katana.print_exception_message")
    def test_loop_up_with_multiple_args_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopUp(0,5) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 11, 1, "0", 0),
            Token(COMMA_TOKEN_TYPE, 12, 1, ",", LOW),
            Token(NUM_TOKEN_TYPE, 13, 1, "5", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 14, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 16, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, TooManyArgsException(1, 4))

    @patch("katana.katana.print_exception_message")
    def test_loop_down_with_multiple_args_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopDown(0,5) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 11, 1, "0", 0),
            Token(COMMA_TOKEN_TYPE, 12, 1, ",", LOW),
            Token(NUM_TOKEN_TYPE, 13, 1, "5", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 14, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 16, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, TooManyArgsException(1, 4))


    @patch("katana.katana.print_exception_message")
    def test_loop_down_with_dot_operator_raises_error(self, mock_print):
        """
        Given a program like:
        ```
        main() {
            loopDown(0..5) {
                print("looping");
            }
        }
        ```
        Expected to raise InvalidArgsException
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(NUM_TOKEN_TYPE, 11, 1, "0", ""),
            Token(RANGE_INDICATION_TOKEN_TYPE, 12, 1, "..", ""),
            Token(NUM_TOKEN_TYPE, 14, 1, "5", ""),
            Token(RIGHT_PAREN_TOKEN_TYPE, 15, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 17, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, InvalidArgsException(1, 4, "loopDown", RangeNode))

    @patch("katana.katana.print_exception_message")
    def test_basic_loop_up_invalid_syntax(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 13, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(1, 4, "loopUp", LOOP_UP_SIGNATURE))


    @patch("katana.katana.print_exception_message")
    def test_basic_loop_down_invalid_syntax(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 13, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(1, 4, "loopDown", LOOP_DOWN_SIGNATURE))

    @patch("katana.katana.print_exception_message")
    def test_basic_loop_from_invalid_syntax(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 10, 1, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 11, 1, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 13, 1, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 8, 2, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 13, 2, "(", 3),
            Token(STRING_TOKEN_TYPE, 14, 2, "Hi", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 18, 2, ")", 3),
            Token(EOL_TOKEN_TYPE, 19, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 3, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 4, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 5, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 4, KeywordMisuseException(1, 4, "loopFrom", LOOP_FROM_SIGNATURE))


class TestKeywordAdvanced:

    def test_if_keyword_with_var_reference_in_conditional(self):
        """
        Given a program like:
        main() {
            int64 x = 1;
            if (x - 1 > 0) {
                print("true");
            } else {
                print("false");
            }
        }
        Expected to return an AST like:
        (main[(int64(x=1)), (if((x-1)>0, print("greater"), None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 6, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 7, "x", 0),
            Token(MINUS_TOKEN_TYPE, 2, 9, "-", 1),
            Token(NUM_TOKEN_TYPE, 2, 11, "1", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 2, 13, ">", 2),
            Token(NUM_TOKEN_TYPE, 2, 15, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 16, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 18, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "true", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 20, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 21, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 4, 11, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 14, "false", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 22, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 8, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[28], "false")
        second_print_node = FunctionKeywordNode(token_list[26], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[20], "true")
        first_print_node = FunctionKeywordNode(token_list[18], "print", [greater_string_node])
        one_node = NumberNode(token_list[7], "1")
        x_node = VariableNode(token_list[5], "x", False)
        x_assignment_node = AssignmentNode(token_list[6], "=", x_node, one_node)
        keyword_node = VariableKeywordNode(token_list[4], "int64", x_assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        one_minus_node = NumberNode(token_list[13], "1")
        subtract_node = PlusMinusNode(token_list[12], "-", x_ref_node, one_minus_node)
        zero_node = NumberNode(token_list[7], "0")
        compare_node = CompareNode(token_list[14], ">", subtract_node, zero_node)
        if_node = LogicKeywordNode(token_list[9], "if", compare_node, None, [first_print_node], [second_print_node])
        ast = StartNode(token_list[0], "main", [keyword_node, if_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_keyword_with_var_reference_in_conditional_right_side(self):
        """
        Given a program like:
        main() {
            int64 x = 1;
            if (0 > x - 1) {
                print("true");
            } else {
                print("false");
            }
        }
        Expected to return an AST like:
        (main[(int64(x=1)), (if(0>(x-1), print("greater"), None)), (print("lower"))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 6, "(", 3),
            Token(NUM_TOKEN_TYPE, 2, 7, "0", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 2, 9, ">", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(MINUS_TOKEN_TYPE, 2, 13, "-", 1),
            Token(NUM_TOKEN_TYPE, 2, 15, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 16, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 18, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "true", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 20, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 21, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 4, 11, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 14, "false", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 22, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 8, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[28], "false")
        second_print_node = FunctionKeywordNode(token_list[26], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[20], "true")
        first_print_node = FunctionKeywordNode(token_list[18], "print", [greater_string_node])
        one_node = NumberNode(token_list[7], "1")
        x_node = VariableNode(token_list[5], "x", False)
        x_assignment_node = AssignmentNode(token_list[6], "=", x_node, one_node)
        keyword_node = VariableKeywordNode(token_list[4], "int64", x_assignment_node)
        x_ref_node = VariableReferenceNode(token_list[13], "x")
        one_minus_node = NumberNode(token_list[15], "1")
        subtract_node = PlusMinusNode(token_list[14], "-", x_ref_node, one_minus_node)
        zero_node = NumberNode(token_list[11], "0")
        compare_node = CompareNode(token_list[12], ">", zero_node, subtract_node)
        if_node = LogicKeywordNode(token_list[9], "if", compare_node, None, [first_print_node], [second_print_node])
        ast = StartNode(token_list[0], "main", [keyword_node, if_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_if_keyword_with_var_reference_in_conditional_both_sides(self):
        """
        Given a program like:
        main() {
            int64 x = 1;
            int64 y = 2;
            if (y - 2 > x - 1) {
                print("true");
            } else {
                print("false");
            }
        }
        Expected to return an AST like:
        (main[(int64(x=1)), (int64(y=2)), (if((y-2)>(x-1), [print("greater")], [(print("lower"))]))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 2, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 2, 10, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 2, 14, "2", 0),
            Token(EOL_TOKEN_TYPE, 2, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 6, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 7, "y", 0),
            Token(MINUS_TOKEN_TYPE, 3, 9, "-", 1),
            Token(NUM_TOKEN_TYPE, 3, 11, "2", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 3, 13, ">", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 15, "x", 0),
            Token(MINUS_TOKEN_TYPE, 3, 17, "-", 1),
            Token(NUM_TOKEN_TYPE, 3, 19, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 20, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 3, 22, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 14, "true", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 20, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 21, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 5, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 5, 11, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 6, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 6, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 6, 14, "false", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 6, 22, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 8, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 9, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[35], "false")
        second_print_node = FunctionKeywordNode(token_list[33], "print", [lower_string_node])
        greater_string_node = StringNode(token_list[27], "true")
        first_print_node = FunctionKeywordNode(token_list[25], "print", [greater_string_node])
        one_node = NumberNode(token_list[7], "1")
        x_node = VariableNode(token_list[5], "x", False)
        x_assignment_node = AssignmentNode(token_list[6], "=", x_node, one_node)
        keyword_node_x = VariableKeywordNode(token_list[4], "int64", x_assignment_node)
        two_node = NumberNode(token_list[12], "2")
        y_node = VariableNode(token_list[10], "y", False)
        y_assignment_node = AssignmentNode(token_list[11], "=", y_node, two_node)
        keyword_node_y = VariableKeywordNode(token_list[9], "int64", y_assignment_node)
        x_ref_node = VariableReferenceNode(token_list[20], "x")
        one_minus_node = NumberNode(token_list[22], "1")
        subtract_node = PlusMinusNode(token_list[21], "-", x_ref_node, one_minus_node)
        y_ref_node = VariableReferenceNode(token_list[16], "y")
        two_minus_node = NumberNode(token_list[18], "2")
        subtract_node_two = PlusMinusNode(token_list[17], "-", y_ref_node, two_minus_node)
        compare_node = CompareNode(token_list[19], ">", subtract_node_two, subtract_node)
        if_node = LogicKeywordNode(token_list[14], "if", compare_node, None, [first_print_node], [second_print_node])
        ast = StartNode(token_list[0], "main", [keyword_node_x, keyword_node_y, if_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_update_var_with_expression(self):
        """
        Given a program like:
        main() {
            int64 x = 1;
            x = x + 3;
        }
        Expected to return an AST like:
        (main[(int64(x=1)), (x=(x+3))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 4, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 6, "=", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 8, "x", 0),
            Token(PLUS_TOKEN_TYPE, 2, 10, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 12, "3", 0),
            Token(EOL_TOKEN_TYPE, 2, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 4, 0, "EOF", 0)
        ]
        one_node = NumberNode(token_list[7], "1")
        x_var_node = VariableNode(token_list[5], "x", False)
        x_assign_node = AssignmentNode(token_list[6], "=", x_var_node, one_node)
        int_keyword_node = VariableKeywordNode(token_list[4], "int64", x_assign_node)
        three_node = NumberNode(token_list[13], "3")
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        plus_node = PlusMinusNode(token_list[12], "+", x_ref_node, three_node)
        x_left_assignmet_ref_node = VariableReferenceNode(token_list[9], "x")
        reassign_node = AssignmentNode(token_list[10], "=", x_left_assignmet_ref_node, plus_node)
        ast = StartNode(token_list[0], "main", [int_keyword_node, reassign_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()


class TestConcatenation:
    """
    Tests related all concatentaion.
    """

    def test_successful_concatenate_char_to_string(self):
        """
        Given a program like:
        ```
        main() {
            string x = "Hello";
            x = x + '!';
        }
        ```
        Expected to return an AST like:
        (main (string(x=Hello)), (x=(x+!)))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 11, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 13, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 15, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 1, 22, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 4, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 6, "=", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 8, "x", 0),
            Token(PLUS_TOKEN_TYPE, 2, 10, "+", 1),
            Token(CHARACTER_TOKEN_TYPE, 2, 13, "!", 0),
            Token(EOL_TOKEN_TYPE, 2, 15, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 4, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[7], "Hello")
        x_dec_node = VariableNode(token_list[5], "x", False)
        x_assign_node = AssignmentNode(token_list[6], "=", x_dec_node, string_node)
        keyword_node = VariableKeywordNode(token_list[4], "string", x_assign_node)
        char_node = CharNode(token_list[13], "!")
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        plus_node = PlusMinusNode(token_list[12], "+", x_ref_node, char_node)
        x_reassign_ref = VariableReferenceNode(token_list[9], "x")
        x_reassign_val_node = AssignmentNode(token_list[10], "=", x_reassign_ref, plus_node)
        ast = StartNode(token_list[0], "main", [keyword_node, x_reassign_val_node])
        parser = Parser(token_list)
        parser.parse()
        assert [ast] == parser.get_nodes()

    def test_concatenate_other_to_string_raises_exception(self):
        """
        Given a program like:
        ```
        main() {
            string x = "Hello";
            x = x + ", Katana!";
        }
        ```
        Expected an exception to be raised for invalid concatenation
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 11, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 13, 1, "=", 2),
            Token(STRING_TOKEN_TYPE, 15, 1, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 22, 1, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 4, 2, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 6, 2, "=", 2),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 8, 2, "x", 0),
            Token(PLUS_TOKEN_TYPE, 10, 2, "+", 1),
            Token(STRING_TOKEN_TYPE, 13, 2, ", Katana!", 0),
            Token(EOL_TOKEN_TYPE, 23, 2, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", 0)
        ]
        parser = Parser(token_list)
        with pytest.raises(InvalidConcatenationException, match="3:8 Cannot concatenate a string with a <class 'katana.katana.StringNode'>."):
            parser.parse()


class TestParserTypeChecking:
    """
    All tests related to checking if a type is valid in the program.
    """

    @patch("katana.katana.print_exception_message")
    def test_setting_int_to_bool_raises_exception(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(BOOLEAN_TOKEN_TYPE, 14, 1, "false", 0),
            Token(EOL_TOKEN_TYPE, 19, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 10, InvalidTypeDeclarationException(1, 10))

    @patch("katana.katana.print_exception_message")
    def test_setting_string_to_bool_raises_exception(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(BOOLEAN_TOKEN_TYPE, 14, 1, "false", 0),
            Token(EOL_TOKEN_TYPE, 19, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 10, InvalidTypeDeclarationException(1, 10))

    @patch("katana.katana.print_exception_message")
    def test_setting_bool_to_int_raises_exception(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "bool", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(NUM_TOKEN_TYPE, 14, 1, "10", 0),
            Token(EOL_TOKEN_TYPE, 19, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 10, InvalidTypeDeclarationException(1, 10))

    @patch("katana.katana.print_exception_message")
    def test_setting_char_to_bool_raises_exception(self, mock_print):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 1, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 10, 1, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 12, 1, "=", 2),
            Token(BOOLEAN_TOKEN_TYPE, 14, 1, "false", 0),
            Token(EOL_TOKEN_TYPE, 19, 1, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", 3),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", 0),
        ]
        parser = Parser(token_list)
        with pytest.raises(SystemExit):
            parser.parse()
        mock_print.assert_called_with([], 10, InvalidTypeDeclarationException(1, 10))


class TestParserVariablesOutsideMain:
    """
    All tests for declaring variables outside of the main method. This serves
    a dual purpose of testing to ensure that `main` not being the first node
    correcly generates a list of ASTs.
    """

    def test_int_before_main(self):
        """
        Given a program like:
        int64 x = 3;
        main() {
            print(x);
        }
        Expected to return node list like:
        [(int64(x=3)), (main[(print[x,])])]
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", 2),
            Token(NUM_TOKEN_TYPE, 0, 10, "3", 0),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 9, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 10, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 12, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0),
        ]
        three_node = NumberNode(token_list[3], "3")
        x_node = VariableNode(token_list[1], "x", False)
        assignment_node = AssignmentNode(token_list[2], "=", x_node, three_node)
        keyword_node = VariableKeywordNode(token_list[0], "int64", assignment_node)
        x_ref_node = VariableReferenceNode(token_list[11], "x")
        print_node = FunctionKeywordNode(token_list[9], "print", [x_ref_node])
        start_node = StartNode(token_list[5], "main", [print_node])
        parser = Parser(token_list)
        parser.parse()
        assert [keyword_node, start_node] == parser.get_nodes()
