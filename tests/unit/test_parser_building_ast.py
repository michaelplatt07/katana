from katana.katana import (ASSIGNMENT_TOKEN_TYPE, COMMENT_TOKEN_TYPE,
                           DIVIDE_TOKEN_TYPE, EOL_TOKEN_TYPE, EQUAL_TOKEN_TYPE,
                           HIGH, KEYWORD_TOKEN_TYPE,
                           LEFT_CURL_BRACE_TOKEN_TYPE, LEFT_PAREN_TOKEN_TYPE,
                           LOW, MEDIUM, MINUS_TOKEN_TYPE, MULTIPLY_TOKEN_TYPE,
                           NUM_TOKEN_TYPE, PLUS_TOKEN_TYPE,
                           RANGE_INDICATION_TOKEN_TYPE,
                           RIGHT_CURL_BRACE_TOKEN_TYPE, RIGHT_PAREN_TOKEN_TYPE,
                           STRING_TOKEN_TYPE, ULTRA_HIGH,
                           VARIABLE_NAME_TOKEN_TYPE,
                           VARIABLE_REFERENCE_TOKEN_TYPE, AssignmentNode,
                           CompareNode, FunctionKeywordNode, LogicKeywordNode,
                           LoopDownKeywordNode, LoopFromKeywordNode,
                           LoopUpKeywordNode, MultiplyDivideNode, NumberNode,
                           Parser, PlusMinusNode, RangeNode, StartNode,
                           StringNode, Token, VariableKeywordNode,
                           VariableNode, VariableReferenceNode)


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


class TestParserVar:
    def test_build_var_dec_and_redec_ast(self):
        # Token list for main method with declaring a single int
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "int8", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 9, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 11, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 13, "3", 0),
            Token(EOL_TOKEN_TYPE, 1, 14, ";", 0),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 2, 4, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 2, 6, "=", 2),
            Token(NUM_TOKEN_TYPE, 2, 8, "4", 0),
            Token(EOL_TOKEN_TYPE, 2, 9, ";", 0),
            Token(KEYWORD_TOKEN_TYPE, 3, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 3, 9, "(", 3),
            Token(VARIABLE_REFERENCE_TOKEN_TYPE, 3, 10, "x", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 3, 11, ")", 3),
            Token(EOL_TOKEN_TYPE, 3, 12, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        # Set up the initial declaration node
        var_name_node = VariableNode(token_list[5], "x", False)
        num_node = NumberNode(token_list[7], "3")
        assignment_node = AssignmentNode(
            token_list[6], "=", left_side=var_name_node, right_side=num_node
        )
        var_type_node = VariableKeywordNode(
            token_list[4], "int8", child_node=assignment_node
        )

        # Set up the redeclaration line
        var_ref_node = VariableReferenceNode(token_list[9], "x")
        new_num_node = NumberNode(token_list[11], "4")
        assignment_node_two = AssignmentNode(
            token_list[10], "=", left_side=var_ref_node, right_side=new_num_node
        )

        # Set up print node
        var_ref_node_two = VariableReferenceNode(token_list[15], "x")
        print_node = FunctionKeywordNode(
            token_list[13], "print", arg_nodes=[var_ref_node_two]
        )

        main_node = StartNode(
            token_list[0],
            token_list[0].value,
            children_nodes=[var_type_node, assignment_node_two, print_node],
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_declare_const_var(self):
        # Token list for main method with declaring a single int
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "const", 4),
            Token(KEYWORD_TOKEN_TYPE, 1, 10, "int8", 4),
            Token(VARIABLE_NAME_TOKEN_TYPE, 1, 15, "x", 0),
            Token(ASSIGNMENT_TOKEN_TYPE, 1, 17, "=", 2),
            Token(NUM_TOKEN_TYPE, 1, 19, "3", 0),
            Token(EOL_TOKEN_TYPE, 1, 20, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 2, 0, "}", 3),
        ]


class TestConditionals:
    def test_if_block_equal_no_else(self):
        # Token list for main method and single line of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 4, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 7, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 8, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 1, 10, "==", 2),
            Token(NUM_TOKEN_TYPE, 1, 13, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 14, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 16, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 8, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 13, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 14, "True", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 20, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 21, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 4, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 4, 0, "}", 3),
        ]

        string_node = StringNode(token_list[13], "True")
        print_node = FunctionKeywordNode(
            token_list[11], "print", arg_nodes=[string_node]
        )

        number_node_one = NumberNode(token_list[6], "1")
        number_node_two = NumberNode(token_list[8], "2")
        compare_node = CompareNode(
            token_list[7], "==", left_side=number_node_one, right_side=number_node_two
        )
        if_node = LogicKeywordNode(
            token_list[4], "if", child_node=compare_node, true_side=[print_node]
        )

        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[if_node]
        )

        parser = Parser(token_list)
        parser.parse()
        assert parser.get_nodes() == [main_node]

    def test_if_block_equal_with_else(self):
        # Token list for main method and single line of code
        token_list = [
            Token(KEYWORD_TOKEN_TYPE, 0, 0, "main", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 0, 4, "(", 3),
            Token(RIGHT_PAREN_TOKEN_TYPE, 0, 5, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 0, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 1, 0, "if", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 1, 3, "(", 3),
            Token(NUM_TOKEN_TYPE, 1, 4, "1", 0),
            Token(EQUAL_TOKEN_TYPE, 1, 6, "==", 2),
            Token(NUM_TOKEN_TYPE, 1, 9, "2", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 1, 10, ")", 3),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 1, 12, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 2, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 2, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 2, 10, "True", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 2, 16, ")", 3),
            Token(EOL_TOKEN_TYPE, 2, 17, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 3, 0, "}", 3),
            Token(KEYWORD_TOKEN_TYPE, 3, 2, "else", 4),
            Token(LEFT_CURL_BRACE_TOKEN_TYPE, 3, 7, "{", 3),
            Token(KEYWORD_TOKEN_TYPE, 4, 4, "print", 4),
            Token(LEFT_PAREN_TOKEN_TYPE, 4, 9, "(", 3),
            Token(STRING_TOKEN_TYPE, 4, 10, "False", 0),
            Token(RIGHT_PAREN_TOKEN_TYPE, 4, 17, ")", 3),
            Token(EOL_TOKEN_TYPE, 4, 18, ";", 0),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 5, 0, "}", 3),
            Token(RIGHT_CURL_BRACE_TOKEN_TYPE, 6, 0, "}", 3),
        ]

        # Set up the expected node list to compare
        one_node = NumberNode(token_list[6], "1")
        two_node = NumberNode(token_list[8], "2")
        compare_node = CompareNode(
            token_list[7], "==", left_side=one_node, right_side=two_node
        )

        true_node = StringNode(token_list[13], "True")
        first_print_node = FunctionKeywordNode(
            token_list[11], "print", arg_nodes=[true_node]
        )

        false_node = StringNode(token_list[21], "False")
        second_print_node = FunctionKeywordNode(
            token_list[19], "print", arg_nodes=[false_node]
        )

        if_node = LogicKeywordNode(
            token_list[4],
            "if",
            child_node=compare_node,
            true_side=[first_print_node],
            false_side=[second_print_node],
        )

        main_node = StartNode(
            token_list[0], token_list[0].value, children_nodes=[if_node]
        )

        parser = Parser(token_list)
        # breakpoint()
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
