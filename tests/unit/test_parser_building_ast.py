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
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    # Nodes
    AssignmentNode,
    MultiplyDivideNode,
    NumberNode,
    PlusMinusNode,
    StartNode,
    VariableKeywordNode,
    VariableNode,
    # Priorities
    LOW,
    MEDIUM,
    HIGH,
    ULTRA_HIGH,
)


class TestParserSingleLine:
    def test_build_addition_line_ast(self):
        # Token list for a single line of code doing addition
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(PLUS_TOKEN_TYPE, 0, 2, "+", MEDIUM),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the ast to compare against
        num_node_one = NumberNode(token_list[0], "8")
        num_node_two = NumberNode(token_list[2], "9")
        addition_node = PlusMinusNode(
            token_list[1], "+", left_side=num_node_one, right_side=num_node_two
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [addition_node]

    def test_build_subtraction_line_ast(self):
        # Token list for a single line of code doing subtraction
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(MINUS_TOKEN_TYPE, 0, 2, "-", MEDIUM),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the ast to compare against
        num_node_one = NumberNode(token_list[0], "8")
        num_node_two = NumberNode(token_list[2], "9")
        subtraction_node = PlusMinusNode(
            token_list[1], "-", left_side=num_node_one, right_side=num_node_two
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [subtraction_node]

    def test_build_multiply_line_ast(self):
        # Token list for a single line of code doing multiplication
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(MULTIPLY_TOKEN_TYPE, 0, 2, "*", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the ast to compare against
        num_node_one = NumberNode(token_list[0], "8")
        num_node_two = NumberNode(token_list[2], "9")
        multiply_node = MultiplyDivideNode(
            token_list[1], "*", left_side=num_node_one, right_side=num_node_two
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [multiply_node]

    def test_build_divide_line_ast(self):
        # Token list for a single line of code doing division
        token_list = [
            Token(NUM_TOKEN_TYPE, 0, 0, "8", LOW),
            Token(DIVIDE_TOKEN_TYPE, 0, 2, "/", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 4, "9", LOW),
            Token(EOL_TOKEN_TYPE, 0, 5, ";", LOW),
        ]

        # Set up the ast to compare against
        num_node_one = NumberNode(token_list[0], "8")
        num_node_two = NumberNode(token_list[2], "9")
        divide_node = MultiplyDivideNode(
            token_list[1], "/", left_side=num_node_one, right_side=num_node_two
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [divide_node]

    def test_build_var_assignment_ast(self):
        # Token list for a single line of code, in this case declaring an int
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 0, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 0, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 0, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 0, 11, ";", LOW),
        ]

        # Set up the ast to compare against
        var_name_node = VariableNode(token_list[1], "x", False)
        num_node = NumberNode(token_list[3], "8")
        assignment_node = AssignmentNode(
            token_list[2], "=", left_side=var_name_node, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[0], "int8", child_node=assignment_node
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [var_type_node]

    def test_build_var_assignment_with_invalid_type(self):
        # TODO(map) Write test cases for:
        # * assign wrong types to int
        # * assign wrong types to string
        # * assign wrong types to char
        # * assign wrong types to bool
        pass


class TestParserComments:
    def test_build_ast_with_comment_on_separate_line(self):
        # Token list for program with comment on separate line
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 6, "{", ULTRA_HIGH),
            Token(COMMENT_TOKEN_TYPE, 1, 0, "// This is a comment", LOW),
            Token(KEYWORD_TOKEN_TYPE, 2, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 2, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 2, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 2, 11, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", ULTRA_HIGH),
        ]

        # Set up the ast to compare to
        var_name_node = VariableNode(token_list[4], "x", False)
        num_node = NumberNode(token_list[6], "8")
        assignment_node = AssignmentNode(
            token_list[5], "=", left_side=var_name_node, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[3], "int8", child_node=assignment_node
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[var_type_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_ast_with_parser_on_same_line(self):
        # Token list for program with comment on same line
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 6, "{", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
            Token(COMMENT_TOKEN_TYPE, 1, 13, "// This is a comment", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", ULTRA_HIGH),
        ]

        # Set up the ast to compare to
        var_name_node = VariableNode(token_list[3], "x", False)
        num_node = NumberNode(token_list[5], "8")
        assignment_node = AssignmentNode(
            token_list[4], "=", left_side=var_name_node, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[2], "int8", child_node=assignment_node
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[var_type_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_ast_with_comment_on_first_line_with_second_line(self):
        # Token list for program with comment on same line and a second line
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", ULTRA_HIGH),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 6, "{", ULTRA_HIGH),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 6, "x", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 1, 10, "8", LOW),
            Token(EOL_TOKEN_TYPE, 1, 11, ";", LOW),
            Token(COMMENT_TOKEN_TYPE, 1, 13, "// This is a comment", LOW),
            Token(KEYWORD_TOKEN_TYPE, 2, 0, "int8", ULTRA_HIGH),
            Token(VARIABLE_NAME_TOKEN_TYPE, 2, 6, "y", LOW),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 8, "=", HIGH),
            Token(NUM_TOKEN_TYPE, 2, 10, "9", LOW),
            Token(EOL_TOKEN_TYPE, 2, 11, ";", LOW),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", ULTRA_HIGH),
        ]

        # Set up the ast to compare to
        var_name_node_one = VariableNode(token_list[3], "x", False)
        num_node_one = NumberNode(token_list[5], "8")
        assignment_node_one = AssignmentNode(
            token_list[4], "=", left_side=var_name_node_one, right_side=num_node_one
        )
        var_type_node_one = VariableKeywordNode(
            token_list[2], "int8", child_node=assignment_node_one
        )

        var_name_node_two = VariableNode(token_list[9], "y", False)
        num_node_two = NumberNode(token_list[11], "9")
        assignment_node_two = AssignmentNode(
            token_list[10], "=", left_side=var_name_node_two, right_side=num_node_two
        )
        var_type_node_two = VariableKeywordNode(
            token_list[8], "int8", child_node=assignment_node_two
        )

        main_node = StartNode(
            token_list[0],
            token_list[0].value,
            children_nodes=[var_type_node_one, var_type_node_two],
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]


class TestParserMain:
    def test_build_main_ast_with_var_dec(self):
        # Token list for main method with declaring a single int
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

        # Set up the ast to compare to
        var_name_node = VariableNode(token_list[3], "x", False)
        num_node = NumberNode(token_list[5], "8")
        assignment_node = AssignmentNode(
            token_list[4], "=", left_side=var_name_node, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[2], "int8", child_node=assignment_node
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[var_type_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_main_ast_with_multiple_var_dec(self):
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

        # Set up the ast to compare to
        var_name_node_one = VariableNode(token_list[3], "x", False)
        num_node_one = NumberNode(token_list[5], "8")
        assignment_node_one = AssignmentNode(
            token_list[4], "=", left_side=var_name_node_one, right_side=num_node_one
        )
        var_type_node_one = VariableKeywordNode(
            token_list[2], "int8", child_node=assignment_node_one
        )
        var_name_node_two = VariableNode(token_list[8], "y", False)
        num_node_two = NumberNode(token_list[10], "9")
        assignment_node_two = AssignmentNode(
            token_list[9], "=", left_side=var_name_node_two, right_side=num_node_two
        )
        var_type_node_two = VariableKeywordNode(
            token_list[7], "int8", child_node=assignment_node_two
        )
        main_node = StartNode(
            token_list[0],
            token_list[0].value,
            children_nodes=[var_type_node_one, var_type_node_two],
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]
