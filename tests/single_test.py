from katana.katana import *


class TestSingleToDebug:

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
        three_node = LiteralNode(token_list[5], "2")
        first_plus = PlusMinusNode(
            token_list[6], "+", two_node, three_node)
        ast = PlusMinusNode(token_list[1], "+", one_node, first_plus)
        parser = Parser(token_list)
        assert ast == parser.parse()
