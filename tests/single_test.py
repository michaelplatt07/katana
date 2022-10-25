from katana.katana import *
class TestSingleToDebug:

    def test_single(self):
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


