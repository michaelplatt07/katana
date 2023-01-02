from katana.katana import (
    KeywordNode,
    LiteralNode,
    MultiplyDivideNode,
    Parser,
    PlusMinusNode,
    StringNode,
    Token,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    STRING_TOKEN_TYPE,
    LOW,
    HIGH,
    MEDIUM,
    VERY_HIGH,
    ULTRA_HIGH,
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
        (3+4)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "3", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "4", LOW),
            Token(COMMENT_TOKEN_TYPE, 8, "// Add numbers", LOW),
            Token(EOF_TOKEN_TYPE, 21, "EOF", LOW),
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

    def test_parser_multiply_sub_add_more_complex(self):
        """
        Given a program like:
        2 * 3 - 4 + 5
        Expected to return an AST like:
        (((2*3)-4)+5)
        """
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, "2", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 2, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 4, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, "4", LOW),
            Token(PLUS_TOKEN_TYPE, 10, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, "5", LOW),
            Token(EOF_TOKEN_TYPE, 13, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "3", LOW),
            Token(MINUS_TOKEN_TYPE, 6, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, "4", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, "5", LOW),
            Token(EOF_TOKEN_TYPE, 13, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 4, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 6, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 8, "4", LOW),
            Token(MINUS_TOKEN_TYPE, 10, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 12, "5", LOW),
            Token(EOF_TOKEN_TYPE, 13, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, "8", LOW),
            Token(DIVIDE_TOKEN_TYPE, 2, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 4, "8", LOW),
            Token(PLUS_TOKEN_TYPE, 6, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 8, "3", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 10, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 12, "2", LOW),
            Token(EOF_TOKEN_TYPE, 13, "EOF", LOW),
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
            Token(NUM_TOKEN_TYPE, 0, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 5, "2", LOW),
            Token(PLUS_TOKEN_TYPE, 7, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 9, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 10, ")", VERY_HIGH),
            Token(EOF_TOKEN_TYPE, 11, "EOF", LOW),
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
            Token(LEFT_PAREN_TOKEN_TYPE, 0, "(", VERY_HIGH),
            Token(NUM_TOKEN_TYPE, 1, "1", LOW),
            Token(PLUS_TOKEN_TYPE, 3, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 5, "2", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 6, ")", VERY_HIGH),
            Token(MULTIPLY_TOKEN_TYPE, 8, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 10, "3", LOW),
            Token(EOF_TOKEN_TYPE, 11, "EOF", LOW),
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
            Token(KEYWORD_TOKEN_TYPE, 0, "print", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 5, "(", HIGH),
            Token(NUM_TOKEN_TYPE, 6, "3", LOW),
            Token(RIGHT_PAREN_TOKEN_TYPE, 7, ")", HIGH),
            Token(EOL_TOKEN_TYPE, 8, ";", LOW),
            Token(NEW_LINE_TOKEN_TYPE, 9, "\n", LOW),
            Token(EOF_TOKEN_TYPE, 10, "EOF", LOW),
        ]
        three_node = LiteralNode(token_list[2], "3")
        ast = KeywordNode(token_list[0], "print", three_node)
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
            Token(STRING_TOKEN_TYPE, 0, "Hello, World!", 0),
            Token(EOL_TOKEN_TYPE, 14, ";", 0),
            Token(NEW_LINE_TOKEN_TYPE, 15, "\n", 0),
            Token(EOF_TOKEN_TYPE, 16, "EOF", 0)
        ]
        ast = StringNode(token_list[0], "Hello, World!")
        parser = Parser(token_list)
        assert ast == parser.parse()
