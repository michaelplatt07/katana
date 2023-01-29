import pytest

from katana.katana import (
    BOOLEAN_TOKEN_TYPE,
    AssignmentNode,
    BooleanNode,
    CompareNode,
    FunctionKeywordNode,
    LiteralNode,
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
    Token,
    ASSIGNMENT_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    LESS_THAN_TOKEN_TYPE,
    GREATER_THAN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
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
)


class TestParserLiterals:

    def test_parser_single_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
        ast = LiteralNode(token_list[0], "1")
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_multi_digit_literal(self):
        token_list = [Token(NUM_TOKEN_TYPE, 0, 1, "123", LOW),
                      Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW)]
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
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 6, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "2", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(MINUS_TOKEN_TYPE, 2, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, 1, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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
        (3+4)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "4", LOW),
            Token(COMMENT_TOKEN_TYPE, 8, 1, "// Add numbers", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        left_node = LiteralNode(token_list[0], "3")
        right_node = LiteralNode(token_list[2], "4")
        ast = PlusMinusNode(token_list[1], "+", left_node, right_node)
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
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
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

    def test_parser_multiply_sub_add_more_complex(self):
        """
        Given a program like:
        2 * 3 - 4 + 5
        Expected to return an AST like:
        (((2*3)-4)+5)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(PLUS_TOKEN_TYPE, 10, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        two_node = LiteralNode(token_list[0], "2")
        three_node = LiteralNode(token_list[2], "3")
        four_node = LiteralNode(token_list[4], "4")
        five_node = LiteralNode(token_list[6], "5")
        multiply_node = MultiplyDivideNode(
            token_list[1], "*", two_node, three_node)
        sub_node = PlusMinusNode(token_list[3], "-", multiply_node, four_node)
        plus_node = PlusMinusNode(token_list[5], "+", sub_node, five_node)
        ast = plus_node
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_add_sub_and_multiply_more_complex(self):
        """
        Given a program like:
        2 + 3 - 4 * 5
        Expected to return an AST like:
        ((2+3)-(4*5))
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        two_node = LiteralNode(token_list[0], "2")
        three_node = LiteralNode(token_list[2], "3")
        four_node = LiteralNode(token_list[4], "4")
        five_node = LiteralNode(token_list[6], "5")
        multiply_node = MultiplyDivideNode(
            token_list[5], "*", four_node, five_node)
        plus_node = PlusMinusNode(token_list[1], "+", two_node, three_node)
        sub_node = PlusMinusNode(token_list[3], "-", plus_node, multiply_node)
        ast = sub_node
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_add_multiply_sub_more_complex(self):
        """
        Given a program like:
        2 + 3 * 4 - 5
        Expected to return an AST like:
        ((2+(3*4))-5)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, 1, "4", LOW),
            Token(MINUS_TOKEN_TYPE, 10, 1, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, 1, "5", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        two_node = LiteralNode(token_list[0], "2")
        three_node = LiteralNode(token_list[2], "3")
        four_node = LiteralNode(token_list[4], "4")
        five_node = LiteralNode(token_list[6], "5")
        multiply_node = MultiplyDivideNode(
            token_list[3], "*", three_node, four_node)
        plus_node = PlusMinusNode(token_list[1], "+", two_node, multiply_node)
        sub_node = PlusMinusNode(token_list[5], "-", plus_node, five_node)
        ast = sub_node
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_parser_div_add_mul_more_complex(self):
        """
        Given a program like:
        8 / 8 + 3 * 2
        Expected to return an AST like:
        ((8*8)+(3*2))
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "8", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, 1, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, 1, "8", LOW),
            Token(PLUS_TOKEN_TYPE, 6, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, 1, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, 1, "2", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        first_eight_node = LiteralNode(token_list[0], "8")
        second_eight_node = LiteralNode(token_list[2], "8")
        three_node = LiteralNode(token_list[4], "3")
        two_node = LiteralNode(token_list[6], "2")
        divide_node = MultiplyDivideNode(
            token_list[1], "/", first_eight_node, second_eight_node)
        multiply_node = MultiplyDivideNode(
            token_list[5], "*", three_node, two_node)
        add_node = PlusMinusNode(
            token_list[3], "+", divide_node, multiply_node)
        ast = add_node
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestParserParenthesis:
    """
    Testing that parenethesis work as expected such as for order of operations.
    """

    def test_simple_add_with_paren(self):
        """
        Given a program like:
        1 + (2 + 3)
        Expected to return an AST like:
        (1+(2+3))
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, 1, "+", MEDIUM),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 7, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 9, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, 1, ")", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        one_node = LiteralNode(token_list[0], "1")
        two_node = LiteralNode(token_list[3], "2")
        three_node = LiteralNode(token_list[5], "3")
        first_plus = PlusMinusNode(
            token_list[4], "+", two_node, three_node)
        ast = PlusMinusNode(token_list[1], "+", one_node, first_plus)
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_add_higher_prio_than_mult_with_paren(self):
        """
        Given a program like:
        (1 + 2) * 3)
        Expected to return an AST like:
        ((1+2)*3)
        """
        token_list = [
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 1, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 1, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 3, 1, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, 1, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, 1, ")", VERY_HIGH),
            Token(MULTIPLY_TOKEN_TYPE, 8, 1, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        one_node = LiteralNode(token_list[1], "1")
        two_node = LiteralNode(token_list[3], "2")
        three_node = LiteralNode(token_list[6], "3")
        first_plus = PlusMinusNode(
            token_list[2], "+", one_node, two_node)
        ast = MultiplyDivideNode(token_list[5], "*", first_plus, three_node)
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestKeywordParser:

    def test_keyword_print_with_literal(self):
        """
        Given a program like:
        print(3)
        Expected to return an AST like:
        (print(3))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 1, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 6, 1, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 1, ")", HIGH),
            Token(EOL_TOKEN_TYPE, 8, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 9, 1, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", LOW),
        ]
        three_node = LiteralNode(token_list[2], "3")
        ast = FunctionKeywordNode(token_list[0], "print", three_node)
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 14, 0, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 1, "EOF", LOW)
        ]
        three_node = LiteralNode(token_list[4], "3")
        ast = StartNode(token_list[0], "main", [three_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_keyword_int_16_declaration(self):
        """
        Given a program like:
        main() {
            int16 x = 3;
        }
        Expected to return an AST like:
        (main[(int16((x=3)))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 8, 0, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int16", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 12, 1, "\n", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 1, 2, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        three_node = LiteralNode(token_list[8], "3")
        x_node = VariableNode(token_list[6], "x")
        assignment_node = AssignmentNode(token_list[7], "=", x_node, three_node)
        keyword_node = VariableKeywordNode(token_list[5], "int16", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_keyword_int_16_reference(self):
        """
        Given a program like:
        main() {
            int16 x = 3;
            print(x);
        }
        Expected to return an AST like:
        (main[(int16((x=3))), (print(x))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 8, 0, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "int16", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 6, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 8, 1, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 10, 1, "3", LOW),
            Token(EOL_TOKEN_TYPE, 11, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 12, 1, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 9, 2, "\n", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 1, 3, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        three_node = LiteralNode(token_list[8], "3")
        x_node = VariableNode(token_list[6], "x")
        assignment_node = AssignmentNode(token_list[7], "=", x_node, three_node)
        variable_dec_node = VariableKeywordNode(token_list[5], "int16", assignment_node)
        x_ref_node = VariableReferenceNode(token_list[13], "x")
        print_node = FunctionKeywordNode(token_list[11], "print", x_ref_node)
        ast = StartNode(token_list[0], "main", [variable_dec_node, print_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_keyword_string_declaration(self):
        """
        Given a program like:
        main() {
            string x = "hello";
        }
        Expected to return an AST like:
        (main[(int16((x="hello")))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 8, 0, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 12, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 13, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 14, 1, "\n", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 1, 2, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        string_node = StringNode(token_list[8], "hello")
        x_node = VariableNode(token_list[6], "x")
        assignment_node = AssignmentNode(token_list[7], "=", x_node, string_node)
        keyword_node = VariableKeywordNode(token_list[5], "string", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

    def test_keyword_string_reference(self):
        """
        Given a program like:
        main() {
            string x = "hello";
            print(x);
        }
        Expected to return an AST like:
        (main[(int16((x=3))), (print(x))])
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 0, "(", VERY_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 0, ")", VERY_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 7, 0, "{", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 8, 0, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "string", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 7, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 9, 1, "=", HIGH),
            Token(STRING_TOKEN_TYPE, 11, 1, "hello", LOW),
            Token(EOL_TOKEN_TYPE, 12, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 13, 1, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 2, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 2, "(", VERY_HIGH),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 6, 2, "x", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, 2, ")", VERY_HIGH),
            Token(EOL_TOKEN_TYPE, 8, 2, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 9, 2, "\n", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 3, "}", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 1, 3, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 4, "EOF", LOW)
        ]
        string_node = StringNode(token_list[8], "hello")
        x_node = VariableNode(token_list[6], "x")
        assignment_node = AssignmentNode(token_list[7], "=", x_node, string_node)
        variable_dec_node = VariableKeywordNode(token_list[5], "string", assignment_node)
        x_ref_node = VariableReferenceNode(token_list[13], "x")
        print_node = FunctionKeywordNode(token_list[11], "print", x_ref_node)
        ast = StartNode(token_list[0], "main", [variable_dec_node, print_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 8, 0, "\n", LOW),
            Token(KEYWORD_TOKEN_TYPE, 0, 1, "bool", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 5, 1, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 7, 1, "=", HIGH),
            Token(BOOLEAN_TOKEN_TYPE, 9, 1, "false", LOW),
            Token(EOL_TOKEN_TYPE, 14, 1, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 14, 1, "\n", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 0, 2, "}", VERY_HIGH),
            Token(NEW_LINE_TOKEN_TYPE, 1, 2, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 0, 3, "EOF", LOW)
        ]
        boolean_node = BooleanNode(token_list[8], "false")
        x_node = VariableNode(token_list[6], "x")
        assignment_node = AssignmentNode(token_list[7], "=", x_node, boolean_node)
        keyword_node = VariableKeywordNode(token_list[5], "bool", assignment_node)
        ast = StartNode(token_list[0], "main", [keyword_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 16, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 5, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 18, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 4, 19, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 5, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[23], "lower")
        second_print_node = FunctionKeywordNode(token_list[21], "print", lower_string_node)
        greater_string_node = StringNode(token_list[15], "greater")
        first_print_node = FunctionKeywordNode(token_list[13], "print", greater_string_node)
        one_node = LiteralNode(token_list[7], "1")
        zero_node = LiteralNode(token_list[9], "0")
        greater_than_node = CompareNode(token_list[8], ">", one_node, zero_node)
        if_node = LogicKeywordNode(token_list[5], "if", greater_than_node, None, [first_print_node], [])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "0", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 16, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 5, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 4, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 18, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 4, 19, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 5, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 6, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[23], "lower")
        second_print_node = FunctionKeywordNode(token_list[21], "print", lower_string_node)
        greater_string_node = StringNode(token_list[15], "greater")
        first_print_node = FunctionKeywordNode(token_list[13], "print", greater_string_node)
        zero_node = LiteralNode(token_list[7], "0")
        one_node = LiteralNode(token_list[9], "1")
        greater_than_node = CompareNode(token_list[8], ">", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[5], "if", greater_than_node, None, [first_print_node], [])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(GREATER_THAN_TOKEN_TYPE, 1, 10, ">", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 16, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "greater still", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 29, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 30, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 3, 31, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 6, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 4, 11, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 4, 12, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 5, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 14, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 21, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 22, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 5, 23, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 6, 5, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 7, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 7, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 8, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[31], "lower")
        second_print_node = FunctionKeywordNode(token_list[29], "print", lower_string_node)
        greater_string_node = StringNode(token_list[15], "greater")
        first_print_node = FunctionKeywordNode(token_list[13], "print", greater_string_node)
        greater_still_string_node = StringNode(token_list[21], "greater still")
        second_first_print_node = FunctionKeywordNode(token_list[19], "print", greater_still_string_node)
        zero_node = LiteralNode(token_list[7], "1")
        one_node = LiteralNode(token_list[9], "0")
        greater_than_node = CompareNode(token_list[8], ">", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[5], "if", greater_than_node, None, [first_print_node, second_first_print_node], [second_print_node])
        ast = StartNode(token_list[0], "main", [if_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(LESS_THAN_TOKEN_TYPE, 1, 10, "<", 2),
            Token(NUM_TOKEN_TYPE, 1, 12, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 15, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 16, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "greater", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 14, "greater still", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 29, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 30, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 3, 31, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 4, 5, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 5, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 5, 10, "lower", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 5, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 5, 18, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 5, 19, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 6, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 7, 0, "EOF", 0)
        ]
        lower_string_node = StringNode(token_list[29], "lower")
        second_print_node = FunctionKeywordNode(token_list[27], "print", lower_string_node)
        greater_string_node = StringNode(token_list[15], "greater")
        first_print_node = FunctionKeywordNode(token_list[13], "print", greater_string_node)
        greater_still_string_node = StringNode(token_list[21], "greater still")
        second_first_print_node = FunctionKeywordNode(token_list[19], "print", greater_still_string_node)
        zero_node = LiteralNode(token_list[7], "1")
        one_node = LiteralNode(token_list[9], "0")
        greater_than_node = CompareNode(token_list[8], "<", zero_node, one_node)
        if_node = LogicKeywordNode(token_list[5], "if", greater_than_node, None, [first_print_node, second_first_print_node])
        ast = StartNode(token_list[0], "main", [if_node, second_print_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 10, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 11, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 14, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 15, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 5, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 4, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[13], "looping")
        print_node = FunctionKeywordNode(token_list[11], "print", string_node)
        three_node = LiteralNode(token_list[7], "3")
        loop_node = LoopUpKeywordNode(token_list[5], "loopUp", three_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 13, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 14, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 16, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 17, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 5, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 4, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[13], "looping")
        print_node = FunctionKeywordNode(token_list[11], "print", string_node)
        three_node = LiteralNode(token_list[7], "3")
        loop_node = LoopDownKeywordNode(token_list[5], "loopDown", three_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        assert ast == parser.parse()

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
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 13, "3", 0),
            Token(RANGE_INDICATION_TOKEN_TYPE, 1, 14, "..", 0),
            Token(NUM_TOKEN_TYPE, 1, 16, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 17, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 18, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 1, 19, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "looping", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 23, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 24, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 25, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 5, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 4, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 5, 0, "EOF", 0)
        ]
        string_node = StringNode(token_list[15], "looping")
        print_node = FunctionKeywordNode(token_list[13], "print", string_node)
        zero_node = LiteralNode(token_list[7], "3")
        three_node = LiteralNode(token_list[9], "3")
        range_node = RangeNode(token_list[8], "..", zero_node, three_node)
        loop_node = LoopFromKeywordNode(token_list[5], "loopFrom", range_node, loop_body=[print_node])
        ast = StartNode(token_list[0], "main", [loop_node])
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestQuotationParser:

    def test_quotation(self):
        """
        Given a program like:
        ""Hello, World!""
        Expected to return an AST like:
        ("Hello, World!")
        """
        token_list = [
            Token(STRING_TOKEN_TYPE, 0, 1, "Hello, World!", 0),
            Token(EOL_TOKEN_TYPE, 14, 1, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 15, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 0, 2, "EOF", 0)
        ]
        ast = StringNode(token_list[0], "Hello, World!")
        parser = Parser(token_list)
        assert ast == parser.parse()


class TestMultiLineParser:

    def test_simple_multi_line(self):
        """
        Given a program like:
        ```
        main() {
            print(1+2);
            print(3+4);
        }
        ```
        Expected to return an AST like:
        (main (print(1+2)), (print(3+4)))
        """
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(NEW_LINE_TOKEN_TYPE, 0, 8, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 9, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 10, "1", 0),
            Token(PLUS_TOKEN_TYPE, 1, 11, "+", 1),
            Token(NUM_TOKEN_TYPE, 1, 12, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 13, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 14, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 1, 15, "\n", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 9, "(", 3),
            Token(NUM_TOKEN_TYPE, 2, 10, "3", 0),
            Token(PLUS_TOKEN_TYPE, 2, 11, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 12, "4", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 13, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 14, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 2, 15, "\n", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
            Token(NEW_LINE_TOKEN_TYPE, 3, 1, "\n", 0),
            Token(EOF_TOKEN_TYPE, 4, 0, "EOF", 0)
        ]

        one_node = LiteralNode(token_list[7], "1")
        two_node = LiteralNode(token_list[9], "2")
        first_plus = PlusMinusNode(token_list[8], "+", one_node, two_node)
        first_print = FunctionKeywordNode(token_list[5], "print", first_plus)

        three_node = LiteralNode(token_list[15], "3")
        four_node = LiteralNode(token_list[17], "4")
        second_plus = PlusMinusNode(token_list[16], "+", three_node, four_node)
        second_print = FunctionKeywordNode(token_list[13], "print", second_plus)

        ast = StartNode(token_list[0], "main", [first_print, second_print])
        parser = Parser(token_list)
        assert ast == parser.parse()
