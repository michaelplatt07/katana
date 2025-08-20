from katana.katana import (
    ASSIGNMENT_TOKEN_TYPE,
    CHARACTER_TOKEN_TYPE,
    COMMA_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    EQUAL_TOKEN_TYPE,
    HIGH,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    LOW,
    MEDIUM,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RANGE_INDICATION_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    STRING_TOKEN_TYPE,
    ULTRA_HIGH,
    VARIABLE_NAME_TOKEN_TYPE,
    VARIABLE_REFERENCE_TOKEN_TYPE,
    ArgSeparatorNode,
    CharNode,
    AssignmentNode,
    CompareNode,
    FunctionKeywordNode,
    LeftCurlBraceNode,
    LeftParenNode,
    LogicKeywordNode,
    LoopDownKeywordNode,
    LoopFromKeywordNode,
    LoopUpKeywordNode,
    MultiplyDivideNode,
    NumberNode,
    Parser,
    PlusMinusNode,
    RangeNode,
    RightCurlBraceNode,
    RightParenNode,
    StartNode,
    StringNode,
    Token,
    VariableKeywordNode,
    VariableNode,
    VariableReferenceNode,
)


class TestParserProcessBlock:
    def test_addition_line(self):
        # Token list for a single line of code doing addition
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(PLUS_TOKEN_TYPE, 0, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            NumberNode(token_list[0], "8"),
            PlusMinusNode(token_list[1], "+"),
            NumberNode(token_list[2], "9"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_subtraction_line(self):
        # Token list for a single line of code doing subtraction
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(MINUS_TOKEN_TYPE, 0, 2, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            NumberNode(token_list[0], "8"),
            PlusMinusNode(token_list[1], "-"),
            NumberNode(token_list[2], "9"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_multiply_line(self):
        # Token list for a single line of code doing multiplication
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 0, 2, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            NumberNode(token_list[0], "8"),
            MultiplyDivideNode(token_list[1], "*"),
            NumberNode(token_list[2], "9"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_divide_line(self):
        # Token list for a single line of code doing division
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(DIVIDE_TOKEN_TYPE, 0, 2, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            NumberNode(token_list[0], "8"),
            MultiplyDivideNode(token_list[1], "/"),
            NumberNode(token_list[2], "9"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_single_line_block_parses(self):
        # Token list for a single line of code, in this case declaring an int
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            VariableKeywordNode(token_list[0], "int8"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "8"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_multiple_lines_block_parses(self):
        # Token list for two lines of code, in this case declaring an int
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "y", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "9", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
        ]

        # Set up the expected node list to compare
        first_expected_node_list = [
            VariableKeywordNode(token_list[0], "int8"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "8"),
        ]
        second_expected_node_list = [
            VariableKeywordNode(token_list[5], "int8"),
            VariableNode(token_list[6], "y", False),
            AssignmentNode(token_list[7], "="),
            NumberNode(token_list[8], "9"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list


class TestParserComments:
    def test_comment_solo_on_line(self):
        # Token list for a single line of code, in this case declaring an int
        token_list = [
            Token(COMMENT_TOKEN_TYPE, 0, 0, "// This is a comment", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = []

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_comment_same_line_as_code(self):
        # Token list for a single line of code with a comment
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", LOW),
            Token(COMMENT_TOKEN_TYPE, 0, 13, "// This is a comment", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
            VariableKeywordNode(token_list[0], "int8"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "8"),
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.curr_block == expected_node_list

        parser.parse_block()
        assert parser.curr_block == []

    def test_comment_after_first_line_with_second_line_present(self):
        # Token list for two lines of code with a comment after the first
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", LOW),
            Token(COMMENT_TOKEN_TYPE, 0, 13, "// This is a comment", LOW),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "y", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "9", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
        ]

        # Set up the expected node list to compare
        first_expected_node_list = [
            VariableKeywordNode(token_list[0], "int8"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "8"),
        ]
        second_expected_node_list = [
            VariableKeywordNode(token_list[6], "int8"),
            VariableNode(token_list[7], "y", False),
            AssignmentNode(token_list[8], "="),
            NumberNode(token_list[9], "9"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == []

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list


class TestParserLoops:
    def test_loop_up_declared(self):
        # Token list for declaring a loop up
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 6, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 7, "8", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 8, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 10, "{", 3),
            Token(NUM_TOKEN_TYPE, 1, 4, "3", 0),
            Token(PLUS_TOKEN_TYPE, 1, 6, "+", 1),
            Token(NUM_TOKEN_TYPE, 1, 8, "5", 0),
            Token(EOL_TOKEN_TYPE, 1, 9, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        loop_up_node = LoopUpKeywordNode(token_list[0], "loopUp")
        first_expected_node_list = [
            loop_up_node,
            NumberNode(token_list[2], "8"),
            LeftCurlBraceNode(token_list[4], token_list[4].value),
        ]
        second_expected_node_list = [
            NumberNode(token_list[5], token_list[5].value),
            PlusMinusNode(token_list[6], token_list[6].value),
            NumberNode(token_list[7], token_list[7].value),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[9], token_list[9].value)
        ]

    def test_loop_down_declared(self):
        # Token list for declaring a loop up
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 8, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 9, "5", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 10, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 12, "{", 3),
            Token(NUM_TOKEN_TYPE, 1, 4, "5", 0),
            Token(PLUS_TOKEN_TYPE, 1, 6, "+", 1),
            Token(NUM_TOKEN_TYPE, 1, 8, "4", 0),
            Token(EOL_TOKEN_TYPE, 1, 9, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        loop_down_node = LoopDownKeywordNode(token_list[0], "loopDown")
        first_expected_node_list = [
            loop_down_node,
            NumberNode(token_list[2], "5"),
            LeftCurlBraceNode(token_list[4], token_list[4].value),
        ]
        second_expected_node_list = [
            NumberNode(token_list[5], token_list[5].value),
            PlusMinusNode(token_list[6], token_list[6].value),
            NumberNode(token_list[7], token_list[7].value),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[9], token_list[9].value)
        ]

    def test_loop_from_declared(self):
        # Token list for declaring a loop up
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 8, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 9, "3", 0),
            Token(RANGE_INDICATION_TOKEN_TYPE, 0, 10, "..", 1),
            Token(NUM_TOKEN_TYPE, 0, 12, "5", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 13, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 15, "{", 3),
            Token(NUM_TOKEN_TYPE, 1, 4, "1", 0),
            Token(PLUS_TOKEN_TYPE, 1, 6, "+", 1),
            Token(NUM_TOKEN_TYPE, 1, 8, "2", 0),
            Token(EOL_TOKEN_TYPE, 1, 9, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        loop_from_node = LoopFromKeywordNode(token_list[0], "loopFrom")
        first_expected_node_list = [
            loop_from_node,
            NumberNode(token_list[2], "3"),
            RangeNode(token_list[3], ".."),
            NumberNode(token_list[4], "5"),
            LeftCurlBraceNode(token_list[6], token_list[6].value),
        ]
        second_expected_node_list = [
            NumberNode(token_list[7], token_list[7].value),
            PlusMinusNode(token_list[8], token_list[8].value),
            NumberNode(token_list[9], token_list[9].value),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[11], token_list[11].value)
        ]


class TestParserPrintFunctionKeyword:
    def test_print_keyword(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 5, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 6, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 7, ")", 3),
            Token(EOL_TOKEN_TYPE, 0, 8, ";", 0),
        ]

        # Set up the expected node list to compare
        print_node = FunctionKeywordNode(token_list[0], "print")
        expected_node_list = [
            print_node,
            NumberNode(token_list[2], "1"),
        ]
        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_printl_keyword(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "printl", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 6, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 7, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 8, ")", 3),
            Token(EOL_TOKEN_TYPE, 0, 9, ";", 0),
        ]

        # Set up the expected node list to compare
        print_node = FunctionKeywordNode(token_list[0], "printl")
        expected_node_list = [
            print_node,
            NumberNode(token_list[2], "1"),
        ]
        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_node_list

    def test_print_with_var_keyword(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", 2),
            Token(NUM_TOKEN_TYPE, 0, 10, "1", 0),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 5, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 1, 6, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 7, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 8, ";", 0),
        ]

        # Set up the expected node list to compare
        first_expected_node_list = [
            VariableKeywordNode(token_list[0], "int64"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "1"),
        ]
        second_expected_node_list = [
            FunctionKeywordNode(token_list[5], "print"),
            VariableReferenceNode(token_list[7], "x"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

    def test_print_with_complex_expression(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", 2),
            Token(NUM_TOKEN_TYPE, 0, 10, "1", 0),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 5, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 1, 6, "x", 0),
            Token(PLUS_TOKEN_TYPE, 1, 8, "+", 1),
            Token(NUM_TOKEN_TYPE, 1, 10, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 12, ";", 0),
        ]

        # Set up the expected node list to compare
        first_expected_node_list = [
            VariableKeywordNode(token_list[0], "int64"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            NumberNode(token_list[3], "1"),
        ]
        second_expected_node_list = [
            FunctionKeywordNode(token_list[5], "print"),
            VariableReferenceNode(token_list[7], "x"),
            PlusMinusNode(token_list[8], "+"),
            NumberNode(token_list[9], "1"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list


class TestConditionals:
    def test_if_block_equal_no_else(self):
        # Token list for main method and single line of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 3, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 4, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 0, 6, "==", 2),
            Token(NUM_TOKEN_TYPE, 0, 9, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 10, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 12, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 1, 10, "True", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 16, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 17, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        first_expected_node_list = [
            LogicKeywordNode(token_list[0], "if"),
            NumberNode(token_list[2], "1"),
            CompareNode(token_list[3], "=="),
            NumberNode(token_list[4], "2"),
        ]
        second_expected_node_list = [
            FunctionKeywordNode(token_list[7], "print"),
            StringNode(token_list[9], "True"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

    def test_if_block_equal_no_else_line_after(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 3, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 4, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 0, 6, "==", 2),
            Token(NUM_TOKEN_TYPE, 0, 9, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 10, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 12, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 1, 10, "True", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 16, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 17, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 0, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 5, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 6, "False", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 13, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 14, ";", 0),
        ]

        # Set up the expected node list to compare
        if_node = LogicKeywordNode(token_list[0], "if")
        first_expected_node_list = [
            if_node,
            NumberNode(token_list[2], "1"),
            CompareNode(token_list[3], "=="),
            NumberNode(token_list[4], "2"),
        ]
        second_expected_node_list = [
            FunctionKeywordNode(token_list[7], "print"),
            StringNode(token_list[9], "True"),
        ]
        third_expected_node_list = [
            FunctionKeywordNode(token_list[13], "print"),
            StringNode(token_list[15], "False"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[12], token_list[12].value)
        ]

        parser.parse_block()
        assert parser.curr_block == third_expected_node_list

    def test_if_block_equal_with_else(self):
        # Token list for main method and single line of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 3, "(", 3),
            Token(NUM_TOKEN_TYPE, 0, 4, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 0, 6, "==", 2),
            Token(NUM_TOKEN_TYPE, 0, 9, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 10, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 12, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 1, 10, "True", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 16, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 17, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 2, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 2, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 3, 10, "False", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        if_node = LogicKeywordNode(token_list[0], "if")
        first_expected_node_list = [
            if_node,
            NumberNode(token_list[2], "1"),
            CompareNode(token_list[3], "=="),
            NumberNode(token_list[4], "2"),
        ]
        second_expected_node_list = [
            FunctionKeywordNode(token_list[7], "print"),
            StringNode(token_list[9], "True"),
        ]
        third_expected_node_list = [
            LogicKeywordNode(token_list[13], "else"),
        ]
        fourth_expected_node_list = [
            FunctionKeywordNode(token_list[15], "print"),
            StringNode(token_list[17], "False"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[12], token_list[12].value)
        ]

        parser.parse_block()
        assert parser.curr_block == third_expected_node_list

        parser.parse_block()
        assert parser.curr_block == fourth_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[20], token_list[20].value)
        ]


class TestParserCharAt:
    def test_char_at(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "char", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 5, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 7, "=", 2),
            Token(KEYWORD_TOKEN_TYPE, 0, 9, "charAt", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 15, "(", 3),
            Token(STRING_TOKEN_TYPE, 0, 16, "Hello", 0),
            Token(COMMA_TOKEN_TYPE, 0, 23, ",", 0),
            Token(NUM_TOKEN_TYPE, 0, 25, "0", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 26, ")", 3),
            Token(EOL_TOKEN_TYPE, 0, 27, ";", 0),
        ]

        expected_node_list = [
            VariableKeywordNode(token_list[0], "char"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            FunctionKeywordNode(token_list[3], "charAt"),
            LeftParenNode(token_list[4], "("),
            StringNode(token_list[5], "Hello"),
            ArgSeparatorNode(token_list[6]),
            NumberNode(token_list[7], "0"),
            RightParenNode(token_list[8], ")"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_node_list


class TestParserUpdateChar:
    def test_update_char(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 7, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 9, "=", 2),
            Token(STRING_TOKEN_TYPE, 0, 11, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 0, 18, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "updateChar", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 10, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 1, 11, "x", 0),
            Token(COMMA_TOKEN_TYPE, 1, 12, ",", 0),
            Token(NUM_TOKEN_TYPE, 1, 14, "0", 0),
            Token(COMMA_TOKEN_TYPE, 1, 15, ",", 0),
            Token(CHARACTER_TOKEN_TYPE, 1, 18, "Q", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 20, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 21, ";", 0),
        ]

        expected_node_list_1 = [
            VariableKeywordNode(token_list[0], "string"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            StringNode(token_list[3], "Hello"),
        ]
        expected_node_list_2 = [
            FunctionKeywordNode(token_list[5], "updateChar"),
            VariableReferenceNode(token_list[7], "x"),
            ArgSeparatorNode(token_list[8]),
            NumberNode(token_list[9], "0"),
            ArgSeparatorNode(token_list[10]),
            CharNode(token_list[11], "Q"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_node_list_1

        parser.parse_block()
        assert parser.curr_block == expected_node_list_2


class TestParserCopyStr:
    def test_copy_str(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 7, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 9, "=", 2),
            Token(STRING_TOKEN_TYPE, 0, 11, "Hello", 0),
            Token(EOL_TOKEN_TYPE, 0, 18, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "string", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 7, "y", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 9, "=", 2),
            Token(STRING_TOKEN_TYPE, 1, 11, "olleH", 0),
            Token(EOL_TOKEN_TYPE, 1, 18, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 0, "copyStr", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 7, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 8, "y", 0),
            Token(COMMA_TOKEN_TYPE, 2, 9, ",", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 11, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 12, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 13, ";", 0),
        ]

        expected_node_list_one = [
            VariableKeywordNode(token_list[0], "string"),
            VariableNode(token_list[1], "x", False),
            AssignmentNode(token_list[2], "="),
            StringNode(token_list[3], "Hello"),
        ]
        expected_node_list_two = [
            VariableKeywordNode(token_list[5], "string"),
            VariableNode(token_list[6], "y", False),
            AssignmentNode(token_list[7], "="),
            StringNode(token_list[8], "olleH"),
        ]
        expected_node_list_three = [
            FunctionKeywordNode(token_list[10], "copyStr"),
            VariableReferenceNode(token_list[12], "y"),
            ArgSeparatorNode(token_list[13]),
            VariableReferenceNode(token_list[14], "x"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_node_list_one

        parser.parse_block()
        assert parser.curr_block == expected_node_list_two

        parser.parse_block()
        assert parser.curr_block == expected_node_list_three


class TestParserTestMain:
    def test_main_loop_declared(self):
        # Token list for main method and single line of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 6, "{", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", ULTRA_HIGH),
        ]

        # Set up the expected node list to compare
        start_node = StartNode(token_list[0], token_list[0].value)
        expected_main_node_list = [
            start_node,
            LeftCurlBraceNode(token_list[1], token_list[1].value),
        ]
        expected_node_list = [
            VariableKeywordNode(token_list[2], "int8"),
            VariableNode(token_list[3], "x", False),
            AssignmentNode(token_list[4], "="),
            NumberNode(token_list[5], "8"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_main_node_list

        parser.parse_block()
        assert parser.curr_block == expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[7], token_list[7].value)
        ]

    def test_main_loop_declared_with_multiple_lines(self):
        # Token list for main method and multiple lines of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 6, "{", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
            Token(KEYWORD_TOKEN_TYPE, 2, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 2, 6, "y", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 2, 10, "9", LOW),
            Token(EOL_TOKEN_TYPE, 2, 11, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", ULTRA_HIGH),
        ]

        # Set up the expected node list to compare
        start_node = StartNode(token_list[0], token_list[0].value)
        expected_main_node_list = [
            start_node,
            LeftCurlBraceNode(token_list[1], token_list[1].value),
        ]
        first_expected_node_list = [
            VariableKeywordNode(token_list[2], "int8"),
            VariableNode(token_list[3], "x", False),
            AssignmentNode(token_list[4], "="),
            NumberNode(token_list[5], "8"),
        ]
        second_expected_node_list = [
            VariableKeywordNode(token_list[7], "int8"),
            VariableNode(token_list[8], "y", False),
            AssignmentNode(token_list[9], "="),
            NumberNode(token_list[10], "9"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.curr_block == expected_main_node_list

        parser.parse_block()
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.curr_block == [
            RightCurlBraceNode(token_list[12], token_list[12].value)
        ]
