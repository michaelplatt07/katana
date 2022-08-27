import argparse
#import pdb
# TODO(map) Move all the classes and enums outs so imports are nice
###########
# Constants
###########
EOF = "EOF"

#############
# Token Types
#############
PLUS_TOKEN_TYPE = "PLUS"
MINUS_TOKEN_TYPE = "MINUS"
NUM_TOKEN_TYPE  = "NUM"
NEW_LINE_TOKEN_TYPE  = "NEWLINE"
SPACE_TOKEN_TYPE  = "SPACE"
EOF_TOKEN_TYPE  = "EOF"

IGNORE_TOKENS = (SPACE_TOKEN_TYPE, NEW_LINE_TOKEN_TYPE)

##########
# Op types
##########
EXP_OP = "EXPRESSION"


#########
# Classes
#########
class Token:
    def __init__(self, ttype, position, value):
        self.ttype = ttype
        self.position = position
        self.value = value

    def __repr__(self):
        return f"[{self.ttype}, {self.position}, {self.value}]"

    def __eq__(self, other):
        return self.ttype == other.ttype and self.position == other.position and self.value == other.value
        
class Node:
    def __init__(self, token):
        self.token = token

class ExpressionNode(Node):
    def __init__(self, token, left_side, right_side):
        super().__init__(token)
        self.left_side = left_side
        self.right_side = right_side

class PlusMinusNode(Node):
    def __init__(self, token, value, left_side=None, right_side=None):
        super().__init__(token)
        self.value = value
        self.left_side = left_side
        self.right_side = right_side

    def __eq__(self, other):
        left_side_equal = self.left_side == other.left_side
        right_side_equal = self.right_side == other.right_side
        return self.value == other.value and left_side_equal and right_side_equal and self.token == other.token

    def __repr__(self):
        return f"({self.left_side}{self.value}{self.right_side})"

class LiteralNode(Node):
    def __init__(self, token, value):
        super().__init__(token)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value and self.token == other.token

    def __repr__(self):
        return f"{self.value}"

class Lexer:
    def __init__(self, program):
        self.start_pos = 0
        self.curr_pos = 0
        self.program = program
        self.end_pos = len(self.program) 
        self.token_list = []
        self.has_next_char = True

    def lex(self):
        while self.has_next_char:
            self.advance()
        return self.token_list

    def advance(self):
        if self.curr_pos == self.end_pos:
            self.has_next_char = False
            self.token_list.append(Token(EOF_TOKEN_TYPE, self.curr_pos, EOF))
        else:
            token = self.generate_token(self.program[self.curr_pos])
            if token.ttype == NUM_TOKEN_TYPE:
                while self.peek().ttype == NUM_TOKEN_TYPE:
                    token.value += self.peek().value
                    self.curr_pos += 1
                    token.position += 1
            if token.ttype not in IGNORE_TOKENS:
                self.token_list.append(token)
            self.curr_pos += 1

    def peek(self) -> Token:
        peek_token = Token(EOF_TOKEN_TYPE, self.curr_pos + 1, EOF)
        if self.curr_pos + 1 < self.end_pos:
            peek_token = self.generate_token(self.program[self.curr_pos + 1])
        return peek_token

    def generate_token(self, character) -> Token:
        if character == '+':
            return Token(PLUS_TOKEN_TYPE, self.curr_pos, character)
        elif character == '-':
            return Token(MINUS_TOKEN_TYPE, self.curr_pos, character)
        elif character.isnumeric():
            return Token(NUM_TOKEN_TYPE, self.curr_pos, character)
        elif character == "\n": # Don't care about return for now
            return Token(NEW_LINE_TOKEN_TYPE, self.curr_pos, character)
        elif character.isspace(): # Never care about spaces
            return Token(SPACE_TOKEN_TYPE, self.curr_pos, character)
        else:
            self.print_invalid_character_error()
            raise Exception("Invalid token")

    def print_invalid_character_error(self):
        print(self.program)
        print(" "*self.curr_pos + "^")

class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.has_next_token = True
        self.curr_token_pos = -1
        self.root_node = None

    def advance_token(self):
        self.curr_token_pos += 1
        self.curr_token = self.token_list[self.curr_token_pos]
        
    def process_token(self):
        node = None
        if self.curr_token.ttype == NUM_TOKEN_TYPE:
            node = self.parse_literal()
        elif self.curr_token.ttype == PLUS_TOKEN_TYPE:
            node = self.parse_op()
        elif self.curr_token.ttype == MINUS_TOKEN_TYPE:
            node = self.parse_op()
        elif self.curr_token.ttype == EOF_TOKEN_TYPE:
            self.has_next_token = False
        return node

    def parse_literal(self):
        node = LiteralNode(self.curr_token, self.curr_token.value)
        if not self.root_node:
            self.root_node = node
        return node

    def parse_op(self):
        node = PlusMinusNode(self.curr_token, self.curr_token.value)
        left_side = self.root_node
        self.root_node = node
        node.left_side = left_side
        self.advance_token()
        right_node = self.process_token()
        self.root_node.right_side = right_node
        return node
    
    def parse(self):
        while self.has_next_token:
            self.advance_token()
            self.process_token()
        return self.root_node
    
######
# main
######
if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--program", help="The program that should be parse.")
    args = arg_parser.parse_args()
    with open(args.program, 'r') as program:
        lexer = Lexer(program.read())
        token_list = lexer.lex()
        print(token_list)
        parser = Parser(token_list)
        print(parser.parse())

