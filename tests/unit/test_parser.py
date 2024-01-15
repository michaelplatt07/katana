
from katana.katana import (
    Parser,
    Token,
    # Tokens
    ASSIGNMENT_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    # Nodes
    AssignmentNode,
    NumberNode,
    VariableKeywordNode,
    VariableNode,
    # Priorities
    LOW,
    HIGH,
    ULTRA_HIGH,
)


class TestParserProcessBlock:

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
        assert parser.is_working_on_line is True
        assert parser.curr_block == expected_node_list

    def test_multiple_lines_block_parses(self):
        pass
