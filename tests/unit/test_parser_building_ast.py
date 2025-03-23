from katana.katana import ASSIGNMENT_TOKEN_TYPE  # Tokens; Nodes; Priorities
from katana.katana import (COMMENT_TOKEN_TYPE, DIVIDE_TOKEN_TYPE,
                           EOL_TOKEN_TYPE, HIGH, KEYWORD_TOKEN_TYPE,
                           LEFT_CURL_BRACE_TOKEN_TYPE, LEFT_PAREN_TOKEN_TYPE,
                           LOW, MEDIUM, MINUS_TOKEN_TYPE, MULTIPLY_TOKEN_TYPE,
                           NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE,
                           RANGE_INDICATION_TOKEN_TYPE,
                           RIGHT_CURL_BRACE_TOKEN_TYPE, RIGHT_PAREN_TOKEN_TYPE,
                           ULTRA_HIGH, VARIABLE_NAME_TOKEN_TYPE,
                           VARIABLE_REFERENCE_TOKEN_TYPE, AssignmentNode,
                           FunctionKeywordNode, LoopDownKeywordNode,
                           LoopFromKeywordNode, LoopUpKeywordNode,
                           MultiplyDivideNode, NumberNode, Parser,
                           PlusMinusNode, RangeNode, StartNode, Token,
                           VariableKeywordNode, VariableNode,
                           VariableReferenceNode)


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


class TestParserLoop:
    def test_build_loop_up_ast(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 4, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopUp", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 10, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 11, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 14, "{", 3),
            Token(NUM_TOKEN_TYPE, 2, 8, "1", 0),
            Token(PLUS_TOKEN_TYPE, 2, 10, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 12, "2", 0),
            Token(EOL_TOKEN_TYPE, 2, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        # Set up the ast to compare to
        num_node_one = NumberNode(token_list[7], token_list[7].value)
        num_node_two = NumberNode(token_list[9], token_list[9].value)
        plus_node = PlusMinusNode(
            token_list[8],
            token_list[8].value,
            left_side=num_node_one,
            right_side=num_node_two,
        )
        loop_arg_node = NumberNode(token_list[4], token_list[4].value)
        loop_up_node = LoopUpKeywordNode(
            token_list[2],
            token_list[2].value,
            child_node=loop_arg_node,
            loop_body=[plus_node],
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[loop_up_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_loop_down_ast(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 4, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopDown", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 11, "3", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 14, "{", 3),
            Token(NUM_TOKEN_TYPE, 2, 8, "1", 0),
            Token(PLUS_TOKEN_TYPE, 2, 10, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 12, "2", 0),
            Token(EOL_TOKEN_TYPE, 2, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        # Set up the ast to compare to
        num_node_one = NumberNode(token_list[7], token_list[7].value)
        num_node_two = NumberNode(token_list[9], token_list[9].value)
        plus_node = PlusMinusNode(
            token_list[8],
            token_list[8].value,
            left_side=num_node_one,
            right_side=num_node_two,
        )
        loop_arg_node = NumberNode(token_list[4], token_list[4].value)
        loop_down_node = LoopDownKeywordNode(
            token_list[2],
            token_list[2].value,
            child_node=loop_arg_node,
            loop_body=[plus_node],
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[loop_down_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_loop_from_ast(self):
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 5, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "loopFrom", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 12, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 13, "3", 0),
            Token(RANGE_INDICATION_TOKEN_TYPE, 1, 14, "..", 1),
            Token(NUM_TOKEN_TYPE, 1, 16, "8", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 17, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 19, "{", 3),
            Token(NUM_TOKEN_TYPE, 2, 8, "1", 0),
            Token(PLUS_TOKEN_TYPE, 2, 10, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 12, "2", 0),
            Token(EOL_TOKEN_TYPE, 2, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        # Set up the ast to compare to
        num_node_one = NumberNode(token_list[9], token_list[9].value)
        num_node_two = NumberNode(token_list[11], token_list[11].value)
        plus_node = PlusMinusNode(
            token_list[10],
            token_list[10].value,
            left_side=num_node_one,
            right_side=num_node_two,
        )
        range_start_node = NumberNode(token_list[4], token_list[4].value)
        range_end_node = NumberNode(token_list[6], token_list[6].value)
        loop_arg_node = RangeNode(
            token_list[5],
            token_list[5].value,
            left_side=range_start_node,
            right_side=range_end_node,
        )
        loop_from_node = LoopFromKeywordNode(
            token_list[2],
            token_list[2].value,
            child_node=loop_arg_node,
            loop_body=[plus_node],
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[loop_from_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]


class TestParserPrintKeyword:
    def test_build_print_ast(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 5, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 9, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 10, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 12, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the ast to compare to
        num_node_one = NumberNode(token_list[4], token_list[4].value)
        print_node = FunctionKeywordNode(
            token_list[2],
            token_list[2].value,
            arg_nodes=[num_node_one],
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[print_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_printl_ast(self):
        # Token list for printl keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 5, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "printl", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 10, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 11, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 12, ")", 3),
            Token(EOL_TOKEN_TYPE, 1, 13, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]

        # Set up the ast to compare to
        num_node_one = NumberNode(token_list[4], token_list[4].value)
        print_node = FunctionKeywordNode(
            token_list[2],
            token_list[2].value,
            arg_nodes=[num_node_one],
        )
        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[print_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_print_with_variable_ref_ast(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 5, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 9, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 10, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 12, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
        ]

        # Set up the ast to compare to
        var_name_nod = VariableNode(token_list[3], "x", False)
        num_node = NumberNode(token_list[5], "1")
        assignment_node = AssignmentNode(
            token_list[4], "=", left_side=var_name_nod, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[2], "int64", child_node=assignment_node
        )
        var_ref_node = VariableReferenceNode(token_list[9], "x")
        print_node = FunctionKeywordNode(
            token_list[7], "print", arg_nodes=[var_ref_node]
        )

        main_node = StartNode(
            token_list[0],
            "main",
            children_nodes=[var_type_node, print_node],
        )

        parser = Parser(token_list)

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_build_print_with_complex_expression_ast(self):
        # Token list for print keywork being called
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 5, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int64", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 10, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 12, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 14, "1", 0),
            Token(EOL_TOKEN_TYPE, 1, 15, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 9, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 10, "x", 0),
            Token(PLUS_TOKEN_TYPE, 2, 12, "+", 1),
            Token(NUM_TOKEN_TYPE, 2, 14, "1", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 15, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 16, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
        ]

        # Set up the ast to compare to
        var_ref_node = VariableReferenceNode(token_list[9], "x")
        num_node = NumberNode(token_list[11], "1")
        plus_node = PlusMinusNode(
            token_list[10], "+", left_side=var_ref_node, right_side=num_node
        )
        var_name_nod = VariableNode(token_list[3], "x", False)
        assignment_node = AssignmentNode(
            token_list[4], "=", left_side=var_name_nod, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[2], "int64", child_node=assignment_node
        )
        print_node = FunctionKeywordNode(token_list[7], "print", arg_nodes=[plus_node])

        main_node = StartNode(
            token_list[0],
            "main",
            children_nodes=[var_type_node, print_node],
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
