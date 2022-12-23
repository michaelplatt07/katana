import argparse
import os
# TODO(map) Move all the classes and enums outs so imports are nice
###########
# Constants
###########
EOF = "EOF"


#######################
# Token/Node Priorities
#######################
ULTRA_HIGH = 4
VERY_HIGH = 3
HIGH = 2
MEDIUM = 1
LOW = 0
NO_OP = None


#############
# Token Types
#############
COMMENT_TOKEN_TYPE = "COMMENT"
DIVIDE_TOKEN_TYPE = "DIVIDE"
MINUS_TOKEN_TYPE = "MINUS"
MULTIPLY_TOKEN_TYPE = "MULTIPLY"
NUM_TOKEN_TYPE = "NUM"
NEW_LINE_TOKEN_TYPE = "NEWLINE"
PLUS_TOKEN_TYPE = "PLUS"
KEYWORD_TOKEN_TYPE = "KEYWORD"
LEFT_PAREN_TOKEN_TYPE = "LEFT_PAREN"
RIGHT_PAREN_TOKEN_TYPE = "RIGHT_PAREN"
SPACE_TOKEN_TYPE = "SPACE"
EOL_TOKEN_TYPE = "EOL"
EOF_TOKEN_TYPE = "EOF"


##############
# Const tuples
##############
ALL_TOKENS = (
    COMMENT_TOKEN_TYPE,
    DIVIDE_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    SPACE_TOKEN_TYPE,
    EOL_TOKEN_TYPE,
    EOF_TOKEN_TYPE
)
IGNORE_TOKENS = (SPACE_TOKEN_TYPE,)
IGNORE_OPS = (
    SPACE_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    EOL_TOKEN_TYPE
)
KEYWORDS = ("print")


############
# Exceptions
############
class UnclosedParenthesisError(Exception):
    def __init__(self):
        super().__init__("Unclosed parenthesis in program.")


# TODO(map) Probably a chance to make the init method more DRY
class InvalidTokenException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid token.")
        self.line_num = line_num
        self.col_num = col_num

    def __str__(self):
        return f"Invalid token at {self.line_num}:{self.col_num}."


class NoTerminatorError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Line is not terminted with a semicolon.")
        self.line_num = line_num
        self.col_num = col_num

    def __str__(self):
        return f"Line {self.line_num}:{self.col_num} must end with a semicolon."


class UnknownKeywordError(Exception):
    def __init__(self, line_num, col_num, keyword):
        super().__init__("Unknown keyword")
        self.line_num = line_num
        self.col_num = col_num
        self.keyword = keyword

    def __str__(self):
        return f"Unknown keyword '{self.keyword}' at {self.line_num}:{self.col_num} in program."

########
# TOKENS
########
class Token:
    def __init__(self, ttype, position, value, priority):
        self.ttype = ttype
        self.position = position
        self.value = value
        self.priority = priority

    def __repr__(self):
        return f"[{self.ttype}, {self.position}, {self.value}, {self.priority}]"

    def __eq__(self, other):
        return (self.ttype == other.ttype
                and self.position == other.position
                and self.value == other.value
                and self.priority == other.priority)


#######
# NODES
#######
class Node:
    """
    Base node class.
    """

    def __init__(self, token, priority, parent_node=None):
        self.token = token
        self.parent_node = parent_node
        # Used to add weight to nodes for checking priority of execution.
        self.priority = priority
        # Used for AST parsing later. Will never be set when building.
        self.visited = False

    def __eq__(self, other):
        priority_equal = self.priority == other.priority
        if not priority_equal:
            assert False, f"{self} priority {self.priority} != {other} priority {other.priority}."

        token_equal = self.token == other.token
        if not token_equal:
            assert False, f"Tokens {self.token} != {other.token}"

        return priority_equal and token_equal


class NoOpNode(Node):
    """
    Node that functionally does nothing. This is in case I want to preserve
    data across the compilation much like with useless tokens.
    """
    def __init__(self,
                 token: Token) -> None:
        self.token: Token = token
        super().__init__(token, NO_OP, None)


class KeywordNode(Node):
    """
    Node for keyword in the Katana language.
    """

    def __init__(self, token, value, child_node, parent_node=None):
        super().__init__(token, ULTRA_HIGH, parent_node)
        self.value = value
        self.child_node = child_node

    def __eq__(self, other):
        child_equal = self.child_node == other.child_node
        values_equal = self.value == other.value
        return child_equal and values_equal and super().__eq__(other)

    def __repr__(self):
        return f"({self.value}({self.child_node}))"


class ExpressionNode(Node):
    """
    Superclass that represents an expression that is some sort of arithmetic.
    """

    def __init__(self, token, value, priority, left_side, right_side,
                 parent_node=None):
        super().__init__(token, priority, parent_node)
        self.value = value
        self.left_side = left_side
        self.right_side = right_side
        self.parent_node = parent_node

        # Set the parent node of the left and right side to self.
        self.left_side.parent_node = self
        self.right_side.parent_node = self

    def __eq__(self, other):
        # Make sure there is a parent on both sides or no parent on either side
        if self.parent_node and not other.parent_node:
            assert False, (f"Found parent node on self {self} but not other {other}")
        elif not self.parent_node and other.parent_node:
            assert False, (f"Found parent node on other {other} but not self {self}")
        elif not self.parent_node and not other.parent_node:
            parents_equal = True
        else:
            parents_equal = (self.parent_node and other.parent_node
                             and self.parent_node.token == other.parent_node.token
                             and self.parent_node.priority == other.parent_node.priority)

        left_side_equal = self.left_side == other.left_side
        right_side_equal = self.right_side == other.right_side
        if not left_side_equal:
            assert False, "Left sides were not equal."
        elif not right_side_equal:
            assert False, "Right sides were not equal."
        elif not parents_equal:
            assert False, "Parents were not equal"

        types_equal = type(self) == type(other)
        if not types_equal:
            assert False, f"Type {type(self)} != {type(other)}"

        values_equal = self.value == other.value
        if not values_equal:
            assert False, f"Value {self.value} != {other.value}"

        return (left_side_equal and right_side_equal and parents_equal and
                types_equal and values_equal and super().__eq__(other))

    def __repr__(self):
        return f"({self.left_side}{self.value}{self.right_side})"


class PlusMinusNode(ExpressionNode):
    """
    Node specific for plus minus. Doing this because of PEMDAS.
    """

    def __init__(self, token, value, left_side=None, right_side=None,
                 parent_node=None):
        super().__init__(token, value, MEDIUM, left_side, right_side,
                         parent_node)

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        if not types_equal:
            assert False, f"Type {type(self)} != {type(other)}"
        return (types_equal and
                super().__eq__(other))


class MultiplyDivideNode(ExpressionNode):
    """
    Node specific for multiply divide. Doing this because of PEMDAS.
    """

    def __init__(self, token, value, left_side=None, right_side=None,
                 parent_node=None):
        super().__init__(token, value, HIGH, left_side, right_side,
                         parent_node)

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        if not types_equal:
            assert False, f"Type {type(self)} != {type(other)}"
        return (types_equal and
                super().__eq__(other))


class LiteralNode(Node):
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        if not types_equal:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal:
            assert False, f"Value {self.value} != {other.value}"
        return (types_equal and values_equal)

    def __repr__(self):
        return f"{self.value}"


#######
# LEXER
#######
class Lexer:
    def __init__(self, program):
        self.start_pos = -1
        self.curr_pos = -1
        self.program = program[0]
        self.end_pos = len(program[0])
        self.token_list = []
        self.has_next_char = True
        self.unpaired_parens = 0

    def lex(self):
        while self.has_next_char:
            self.advance()
        if self.unpaired_parens != 0:
            raise UnclosedParenthesisError()
        return self.token_list

    def advance(self):
        self.curr_pos += 1
        if self.curr_pos == self.end_pos:
            self.has_next_char = False
            self.token_list.append(
                Token(EOF_TOKEN_TYPE, self.curr_pos, EOF, LOW))
        else:
            token = self.generate_token(self.program[self.curr_pos])
            if token.ttype == NUM_TOKEN_TYPE:
                while self.peek().ttype == NUM_TOKEN_TYPE:
                    token.value += self.peek().value
                    self.curr_pos += 1
                    token.position += 1
            elif token.ttype == DIVIDE_TOKEN_TYPE:
                if self.peek().ttype == DIVIDE_TOKEN_TYPE:
                    token = self.get_single_line_comment_token()
            elif token.ttype == LEFT_PAREN_TOKEN_TYPE:
                self.unpaired_parens += 1
            elif token.ttype == RIGHT_PAREN_TOKEN_TYPE:
                self.unpaired_parens -= 1
            if token.ttype not in IGNORE_TOKENS:
                self.token_list.append(token)

    def peek(self) -> Token:
        peek_token = Token(EOF_TOKEN_TYPE, self.curr_pos + 1, EOF, LOW)
        if self.curr_pos + 1 < self.end_pos:
            peek_token = self.generate_token(self.program[self.curr_pos + 1])
        return peek_token

    def get_single_line_comment_token(self) -> Token:
        end_of_comment_pos = self.program[self.curr_pos:].index(
            "\n") + self.curr_pos
        token = Token(COMMENT_TOKEN_TYPE, self.curr_pos,
                      self.program[self.curr_pos:end_of_comment_pos], LOW)
        self.curr_pos = end_of_comment_pos
        return token

    def generate_token(self, character) -> Token:
        try:
            if character.isnumeric():
                return Token(NUM_TOKEN_TYPE, self.curr_pos, character, LOW)
            elif character == '+':
                return Token(PLUS_TOKEN_TYPE, self.curr_pos, character, MEDIUM)
            elif character == '-':
                return Token(MINUS_TOKEN_TYPE, self.curr_pos, character, MEDIUM)
            elif character == '*':
                return Token(MULTIPLY_TOKEN_TYPE, self.curr_pos, character, HIGH)
            elif character == '/':
                return Token(DIVIDE_TOKEN_TYPE, self.curr_pos, character, HIGH)
            elif character == '(':
                return Token(LEFT_PAREN_TOKEN_TYPE, self.curr_pos, character, VERY_HIGH)
            elif character == ')':
                return Token(RIGHT_PAREN_TOKEN_TYPE, self.curr_pos, character, VERY_HIGH)
            elif character == ';':
                return Token(EOL_TOKEN_TYPE, self.curr_pos, character, LOW)
            elif character.isalpha():
                return self.generate_keyword_token()
            elif character == "\n":  # Don't care about return for now
                if self.token_list[len(self.token_list) - 1].ttype != EOL_TOKEN_TYPE:
                    # Increment by one so we show the arrow at the end of line.
                    raise NoTerminatorError(1, self.curr_pos + 1)
                return Token(NEW_LINE_TOKEN_TYPE, self.curr_pos, character, LOW)
            elif character.isspace():  # Never care about spaces
                return Token(SPACE_TOKEN_TYPE, self.curr_pos, character, LOW)
            else:
                raise InvalidTokenException(1, self.curr_pos)
        except NoTerminatorError as nte:
            self.print_invalid_character_error()
            print(nte)
            exit(1)
        except InvalidTokenException as ite:
            self.print_invalid_character_error()
            print(ite)
            exit(1)
        except UnknownKeywordError as uke:
            self.print_invalid_character_error()
            print(uke)
            exit(1)

    def generate_keyword_token(self):
        keyword = ""
        original_pos = self.curr_pos
        while self.program[self.curr_pos].isalpha():
            keyword += self.program[self.curr_pos]
            # TODO(map) De-couple the advance from generating the token
            self.curr_pos += 1

        # TODO(map) This is a dirty hack and will be resolved when I decouple
        # the problem in the TODO above.
        self.curr_pos -= 1
        if keyword not in KEYWORDS:
            raise UnknownKeywordError(1, original_pos, keyword)
        return Token(KEYWORD_TOKEN_TYPE, original_pos, keyword, ULTRA_HIGH)

    def print_invalid_character_error(self):
        print(self.program)
        print(" "*self.curr_pos + "^")


########
# PARSER
########
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.has_next_token = True
        self.curr_token_pos = -1
        self.root_node = None

    def parse(self):
        root_node = None
        while self.has_next_token:
            self.advance_token()
            node = self.process_token(root_node)
            if node and type(node) != NoOpNode:
                root_node = node
        return root_node

    def advance_token(self):
        self.curr_token_pos += 1
        self.curr_token = self.token_list[self.curr_token_pos]

    def process_token(self, root_node):
        node = None
        if self.curr_token.ttype == NUM_TOKEN_TYPE:
            node = self.parse_literal()
        elif self.curr_token.ttype == PLUS_TOKEN_TYPE:
            node = self.parse_op(PlusMinusNode, root_node)
        elif self.curr_token.ttype == MINUS_TOKEN_TYPE:
            node = self.parse_op(PlusMinusNode, root_node)
        elif self.curr_token.ttype == MULTIPLY_TOKEN_TYPE:
            node = self.parse_op(MultiplyDivideNode, root_node)
        elif self.curr_token.ttype == DIVIDE_TOKEN_TYPE:
            node = self.parse_op(MultiplyDivideNode, root_node)
        elif self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            node = self.handle_parenthesis()
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE:
            node = self.handle_keyword()
        elif self.curr_token.ttype in IGNORE_OPS:
            node = NoOpNode(self.curr_token)
        elif self.curr_token.ttype == EOF_TOKEN_TYPE:
            node = NoOpNode(self.curr_token)
            self.has_next_token = False
        else:
            assert False, f"Unknown token type {self.curr_token.ttype}"
        return node

    def parse_literal(self):
        """
        Parse a literal token.

        If we are parsing a literal token we create it but don't set the
        parent_node because it will either get set later in the parse_op on
        the creation of the op node, or it isn't linked to anything anyways.
        """
        return LiteralNode(self.curr_token, self.curr_token.value, None)

    def parse_op(self, op_type, root_node):
        # This determines whether or not the root node is an operation or a
        # number and if we should replace the right side with an op
        replace_right_side_with_op = (
                type(root_node) != LiteralNode
                and root_node.priority < self.curr_token.priority
                and self.token_list[self.curr_token_pos-1].priority < self.curr_token.priority
                )
        if replace_right_side_with_op:
            left_node = root_node.right_side
        else:
            left_node = root_node
        op_token = self.curr_token
        self.advance_token()
        right_node = self.process_token(root_node)
        node = op_type(op_token, op_token.value,
                       left_side=left_node, right_side=right_node)
        if replace_right_side_with_op:
            ret_node = root_node
            node.parent_node = ret_node
            ret_node.right_side = node
            return ret_node
        return node

    def handle_parenthesis(self):
        # This only works for numbers. For functions this will need to be
        # updated to handle those situations.
        root_node = None
        if self.token_list[self.curr_token_pos - 1].ttype in ALL_TOKENS:
            # Advance once to get past the paren token.
            self.advance_token()

            # Currently don't care about the previous token. Keeping this in
            # so we can error out if the token isn't recognized.
            while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
                root_node = self.process_token(root_node)
                self.advance_token()
        else:
            assert False, f"Token {self.token_list[self.curr_token_pos - 1]} not in ALL_TOKENS"
        return root_node


    def handle_keyword(self):
        root_node = None
        keyword_node = KeywordNode(self.curr_token, self.curr_token.value, None, None)
        # Move past keyword token
        self.advance_token()
        # Move past the parenthesis
        self.advance_token()
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
                root_node = self.process_token(root_node)
                self.advance_token()

        keyword_node.child_node = root_node
        root_node.parent_node = keyword_node
        return keyword_node


##########
# Compiler
##########
class Compiler:

    def __init__(self, ast):
        self.ast = ast
        self.output_path = os.getcwd() + "/out.asm"

    def compile(self):
        self.create_empty_out_file()
        self.create_keyword_functions()
        self.create_assembly_skeleton()
        self.write_assembly()
        self.create_assembly_for_exit()

    def create_empty_out_file(self):
        with open(self.output_path, 'w') as compiled_program:
            compiled_program.write(";; Start of program\n")

    def write_assembly(self):
        with open(self.output_path, 'a') as compiled_program:
            for line in self.traverse_tree(self.ast):
                compiled_program.write(line)

    def traverse_tree(self, node):
        if type(node) is LiteralNode:
            node.visited = True
            print(f"Pushing {node.value} onto stack.")
            return self.get_push_number_onto_stack_asm(node.value) + self.traverse_tree(node.parent_node)
        elif type(node) is KeywordNode and not node.visited:
            node.visited = True
            return self.traverse_tree(node.child_node)
        elif type(node) is KeywordNode and node.visited:
            return self.get_keyword_asm()
        # TODO(map) This should maybe all be under the condition for ExpressionNodes
        elif node.left_side and not node.left_side.visited:
            print(
                f"Traversing from {node} to left side node {node.left_side}")
            return self.traverse_tree(node.left_side)
        elif node.right_side and not node.right_side.visited:
            print(
                f"Traversing from {node} to right side node {node.right_side}")
            return self.traverse_tree(node.right_side)
        elif node.left_side.visited and node.right_side.visited and node.parent_node:
            node.visited = True
            print(f"Performing node {node.value} op for {node}.")
            if node.value == "+":
                return self.get_add_asm() + self.traverse_tree(node.parent_node)
            elif node.value == "-":
                return self.get_sub_asm() + self.traverse_tree(node.parent_node)
            elif node.value == "*":
                return self.get_mul_asm() + self.traverse_tree(node.parent_node)
            elif node.value == "/":
                return self.get_div_asm() + self.traverse_tree(node.parent_node)
            else:
                assert False, f"Unrecognized node value {node.value}"
        elif not node.parent_node:
            print(f"Performing root node {node.value} op.")
            if node.value == "+":
                return self.get_add_asm()
            elif node.value == "-":
                return self.get_sub_asm()
            elif node.value == "*":
                return self.get_mul_asm()
            elif node.value == "/":
                return self.get_div_asm()
            else:
                assert False, f"Unrecognized root node value {node.value}"
        else:
            assert False, (f"This node type {type(node)} is"
                           "not yet implemented.")

    def create_keyword_functions(self):
        # TODO(map) I should do a check to see if the section text already exits.
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    print:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Do the print with the value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        add rax, 48\n")
            compiled_program.write("        push rax\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")


    def create_assembly_skeleton(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("    global _start\n")
            compiled_program.write("        _start:\n")

    def get_push_number_onto_stack_asm(self, num):
        return [f"    push {num}\n"]

    def get_add_asm(self):
        return ["    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n"]

    def get_sub_asm(self):
        return ["    ;; Subtract\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    sub rbx, rax\n",
                "    push rbx\n"]

    def get_mul_asm(self):
        return ["    ;; Multiply\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    mul rbx\n",
                "    push rax\n"]

    def get_div_asm(self):
        return ["    ;; Divide\n",
                "    pop rbx\n",
                "    pop rax\n",
                "    div rbx\n",
                "    push rax\n"]

    # TODO(map) I think I need two lists here, the variables and text of the code.
    def get_keyword_asm(self):
        return ["    ;; Keyword Func\n",
                "    call print\n"
                ]

    def create_assembly_for_exit(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("    ;; Exit\n")
            compiled_program.write("    mov rax, 60\n")
            compiled_program.write("    mov rdi, 0\n")
            compiled_program.write("    syscall\n")


def run_program():
    os.system("nasm -f elf64 out.asm")
    os.system("ld -o out out.o")
    os.system("./out")


######
# main
######
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--program", help="The program that should be parse.")
    arg_parser.add_argument("--lex", action="store_true",
                            help="Lex the program and return a token list.")
    arg_parser.add_argument("--parse", action="store_true",
                            help="Return the program and print the AST.")
    arg_parser.add_argument("--compile", action="store_true",
                            help="Compile the program and create assembly.")
    arg_parser.add_argument("--run", action="store_true",
                            help="Run the assembled program.")
    args = arg_parser.parse_args()

    with open(args.program, 'r') as program:
        token_list = None
        ast = None
        if args.lex or args.parse or args.compile or args.run:
            lines = program.readlines()
            if len(lines) > 1:
                assert False, "Multi-line processing not enabled."
            lexer = Lexer(lines)
            token_list = lexer.lex()
            print(token_list)
        if args.parse or args.compile or args.run:
            parser = Parser(token_list)
            ast = parser.parse()
            print(ast)
        if args.compile or args.run:
            compiler = Compiler(ast)
            compiler.compile()
        if args.run:
            run_program()
