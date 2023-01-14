from katana.katana import (
    AssignmentNode,
    FunctionKeywordNode,
    KeywordNode,
    LiteralNode,
    MultiplyDivideNode,
    Parser,
    PlusMinusNode,
    StartNode,
    StringNode,
    VariableNode,
    VariableKeywordNode,
    Token,
    ASSIGNMENT_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    STRING_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
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
        (main[(x=3])

        token, value, child_node, parent_node
        KeywordNode()
            - token = keyword int16
            - value = int16
            - Parent node = main
            - Child node = AssignmentNode
        AssignmentNode() <- Similar to an OpNode
            - token = assignment token type
            - left_side = variable
            - right_side = literal/string
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
        x = parser.parse()
        assert ast == x

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
