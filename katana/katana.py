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
NUM_TOKEN_TYPE  = "NUM"
NEW_LINE_TOKEN_TYPE  = "NEWLINE"
SPACE_TOKEN_TYPE  = "SPACE"
EOF_TOKEN_TYPE  = "EOF"

IGNORE_TOKENS = (SPACE_TOKEN_TYPE, NEW_LINE_TOKEN_TYPE)

##########
# Op types
##########
EXP_OP = "EXPRESSION"

##########
# Literals
##########

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

class OpNode(Node):
    def __init__(self, token, value, left_side=None, right_side=None):
        super().__init__(token)
        self.value = value
        self.left_side = left_side
        self.right_side = right_side

    def __eq__(self, other):
        left_side_equal = self.left_side == other.left_side
        right_side_equal = self.right_side == other.right_side
        return self.value == other.value and left_side_equal and right_side_equal

class LiteralNode(Node):
    def __init__(self, token, value):
        super().__init__(token)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

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

"""
input: 1+2
      +
    1   2
Given list of tokens start reading
for first token only
create and set ast root to node

if token type is operation
create op node
set ast root to op node
add prev node to left side of op node
continue

if token type is Literal
add node to the op node right side


input: 1 + 2 - 3
        -
      +   3
   1   2
if token type is minus
create op node minus and set ast root as op node minus

input: 1
       1
Given list of tokens start reading
for first token only
create node and set ast root to node
"""
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.has_next_token = True
        self.curr_token_pos = -1
        self.root_node = None

    def advance_token(self):
        self.curr_token_pos += 1
        self.curr_token = self.token_list[self.curr_token_pos]
        if not self.root_node:
            self.root_node = self.process_token()
        else:
            self.process_token()

    def process_token(self):
        node = None
        if self.curr_token.ttype == NUM_TOKEN_TYPE:
            node = self.parse_literal()
            if self.root_node and self.root_node.token.ttype == PLUS_TOKEN_TYPE and self.root_node.left_side:
                self.root_node.right_side = node
        elif self.curr_token.ttype == PLUS_TOKEN_TYPE:
            node = self.parse_op()
        elif self.curr_token.ttype == EOF_TOKEN_TYPE:
            self.has_next_token = False
        return node

    def parse_literal(self):
        return LiteralNode(self.curr_token, self.curr_token.value)

    def parse_op(self):
        node = OpNode(self.curr_token, self.curr_token.value)
        if self.root_node and self.root_node.token.ttype == NUM_TOKEN_TYPE:
            left_side = self.root_node
            self.root_node = node
            node.left_side = left_side
        return node

    
    def parse(self):
        while self.has_next_token:
            self.advance_token()

        return self.root_node
    
if __name__=="__main__":
    with open('/home/michael/Desktop/programming/katana/sample_programs/addition.ktna', 'r') as program:
        lexer = Lexer(program.read())
        # lexer.lex()
        print(lexer.lex())

