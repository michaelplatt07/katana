import pytest
from katana.katana import (
    DIVIDE_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    Lexer,
    LiteralNode,
    MINUS_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    MultiplyDivideNode,
    Parser,
    PlusMinusNode,
    Token,
    HIGH,
    MEDIUM,
    LOW
)


class TestCompilerAddSubOnly:
    def test_simple_math_program(self):
        """
        Given a simple mathmatics program like:
        1 + 2 + 3 - 4
        Expected result of:
        (((1+2)+3)-4)
        """
        lexer = Lexer("1 + 2 + 3 - 4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3", LOW), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 12, "4", LOW), "4")
        plus_node_one = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM), "+", literal_one, literal_two
        )
        plus_node_two = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 6, "+",
                  MEDIUM), "+", plus_node_one, literal_three
        )
        minus_node_one = PlusMinusNode(
            Token(MINUS_TOKEN_TYPE, 10, "-",
                  MEDIUM), "-", plus_node_two, literal_four
        )
        expected_ast = minus_node_one
        assert expected_ast == parser.parse()

    def test_simple_math_program_bad_format(self):
        """
        Given a simple mathmatics program with extra spaces like:
        1 +      2  +     3 -      4
        Expected result of:
        (((1+2)+3)-4)
        """
        lexer = Lexer("1 +      2  +     3 -      4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 9, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 18, "3", LOW), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 27, "4", LOW), "4")
        plus_node_one = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 2, "+", MEDIUM), "+", literal_one, literal_two
        )
        plus_node_two = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 12, "+",
                  MEDIUM), "+", plus_node_one, literal_three
        )
        minus_node_one = PlusMinusNode(
            Token(MINUS_TOKEN_TYPE, 20, "-",
                  MEDIUM), "-", plus_node_two, literal_four
        )
        expected_ast = minus_node_one
        assert expected_ast == parser.parse()


class TestCompilerMultDivOnly:
    def test_simple_multiply(self):
        """
        Given a simple mathmatics program like:
        1 * 2 * 3
        Expected result of:
        ((1*2)*3)
        """
        lexer = Lexer("1 * 2 * 3\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3", LOW), "3")
        mul_node_one = MultiplyDivideNode(
            Token(MULTIPLY_TOKEN_TYPE, 2, "*",
                  HIGH), "*", literal_one, literal_two
        )
        mul_node_two = MultiplyDivideNode(
            Token(MULTIPLY_TOKEN_TYPE, 6, "*",
                  HIGH), "*", mul_node_one, literal_three
        )
        expected_ast = mul_node_two
        assert expected_ast == parser.parse()

    def test_simple_divide(self):
        """
        Given a simple mathmatics program like:
        1 / 2 / 3
        Expected result of:
        ((1/2)/3)
        """
        lexer = Lexer("1 / 2 / 3\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3", LOW), "3")
        div_node_one = MultiplyDivideNode(
            Token(DIVIDE_TOKEN_TYPE, 2, "/",
                  HIGH), "/", literal_one, literal_two
        )
        div_node_two = MultiplyDivideNode(
            Token(DIVIDE_TOKEN_TYPE, 6, "/",
                  HIGH), "/", div_node_one, literal_three
        )
        expected_ast = div_node_two
        assert expected_ast == parser.parse()


class TestCompilerAdvancedMath:
    def test_mul_add_div_program(self):
        """
        Given a simple mathmatics program like:
        1 * 2 + 3 / 4
        Expected result of:
        ((1+2)-(4*3))
        """
        lexer = Lexer("1 * 2 + 3 / 4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3", LOW), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 12, "4", LOW), "4")
        mul_node = MultiplyDivideNode(
            Token(MULTIPLY_TOKEN_TYPE, 2, "*",
                  HIGH), "*", literal_one, literal_two
        )
        div_node = MultiplyDivideNode(
            Token(DIVIDE_TOKEN_TYPE, 10, "/",
                  HIGH), "/", literal_three, literal_four
        )
        plus_node = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 6, "+", MEDIUM), "+", mul_node, div_node
        )
        expected_ast = plus_node
        assert expected_ast == parser.parse()

    def test_add_sub_div_program(self):
        """
        Given a simple mathmatics program like:
        1 + 2 - 3 / 4
        Expected result of:
        ((1+2)-(3/4))
        """
        lexer = Lexer("1 + 2 - 3 / 4\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        literal_one = LiteralNode(Token(NUM_TOKEN_TYPE, 0, "1", LOW), "1")
        literal_two = LiteralNode(Token(NUM_TOKEN_TYPE, 4, "2", LOW), "2")
        literal_three = LiteralNode(Token(NUM_TOKEN_TYPE, 8, "3", LOW), "3")
        literal_four = LiteralNode(Token(NUM_TOKEN_TYPE, 12, "4", LOW), "4")
        plus_node = PlusMinusNode(
            Token(PLUS_TOKEN_TYPE, 2, "+",
                  MEDIUM), "+", literal_one, literal_two
        )
        div_node = MultiplyDivideNode(
            Token(DIVIDE_TOKEN_TYPE, 10, "/",
                  HIGH), "/", literal_three, literal_four
        )
        minus_node = PlusMinusNode(
            Token(MINUS_TOKEN_TYPE, 6, "-", MEDIUM), "-", plus_node, div_node
        )
        expected_ast = minus_node
        assert expected_ast == parser.parse()


class TestParenthesis:

    def test_add_higher_prio_than_mult_with_paren(self):
        """
        Given a program like:
        (1 + 2) * 3)
        Expected to return an AST like:
        ((1+2)*3)
        """
        lexer = Lexer("(1 + 2) * 3\n")
        token_list = lexer.lex()
        parser = Parser(token_list)
        one_node = LiteralNode(token_list[1], "1")
        two_node = LiteralNode(token_list[3], "2")
        three_node = LiteralNode(token_list[6], "3")
        first_plus = PlusMinusNode(
            token_list[2], "+", one_node, two_node)
        ast = MultiplyDivideNode(token_list[5], "*", first_plus, three_node)
        parser = Parser(token_list)
        assert ast == parser.parse()
