
from katana.katana import (
    Parser,
    Token,
    # Tokens
    ASSIGNMENT_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    # Nodes
    AssignmentNode,
    LeftCurlBraceNode,
    MultiplyDivideNode,
    NumberNode,
    PlusMinusNode,
    RightCurlBraceNode,
    StartNode,
    VariableKeywordNode,
    VariableNode,
    # Priorities
    LOW,
    MEDIUM,
    HIGH,
    ULTRA_HIGH,
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
        assert parser.nested_nodes_list == []
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
        assert parser.nested_nodes_list == []
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
        assert parser.nested_nodes_list == []
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
        assert parser.nested_nodes_list == []
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
            NumberNode(token_list[3], "8")
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.nested_nodes_list == []
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
            NumberNode(token_list[8], "9")
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == second_expected_node_list


class TestParserComments:

    def test_comment_solo_on_line(self):
        # Token list for a single line of code, in this case declaring an int
        token_list = [
            Token(COMMENT_TOKEN_TYPE, 0, 0, "// This is a comment", LOW),
        ]

        # Set up the expected node list to compare
        expected_node_list = [
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.nested_nodes_list == []
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
            NumberNode(token_list[3], "8")
        ]

        parser = Parser(token_list)
        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == []
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
            NumberNode(token_list[9], "9")
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == []

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == second_expected_node_list


class TestParserLoops:

    def test_loop_up_declared(self):
        # Token list for declaring a loop up
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "loopUp", ULTRA_HIGH),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 0, "(", ULTRA_HIGH),
            Token(NUM_TOKEN_TYPE, 0, 0, "8", ULTRA_HIGH),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 0, ")", LOW),
        ]
        assert False, "Not implemented"

    def test_loop_down_declared(self):
        assert False, "Not implemented"

    def test_loop_from_declared(self):
        assert False, "Not implemented"


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
            LeftCurlBraceNode(token_list[1], token_list[1].value)
        ]
        expected_node_list = [
            VariableKeywordNode(token_list[2], "int8"),
            VariableNode(token_list[3], "x", False),
            AssignmentNode(token_list[4], "="),
            NumberNode(token_list[5], "8"),
        ]

        parser = Parser(token_list)

        parser.parse_block()
        assert parser.nested_nodes_list == [start_node]
        assert parser.curr_block == expected_main_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == [start_node]
        assert parser.curr_block == expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == [RightCurlBraceNode(
            token_list[7], token_list[7].value)]

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
            LeftCurlBraceNode(token_list[1], token_list[1].value)
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
        assert parser.nested_nodes_list == [start_node]
        assert parser.curr_block == expected_main_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == [start_node]
        assert parser.curr_block == first_expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == [start_node]
        assert parser.curr_block == second_expected_node_list

        parser.parse_block()
        assert parser.nested_nodes_list == []
        assert parser.curr_block == [RightCurlBraceNode(
            token_list[12], token_list[12].value)]
