import argparse
import os
# TODO(map) Move all the classes and enums outs so imports are nice
#########
# GLOBALS
#########
verbose_flag = False

###########
# Constants
###########
EOF = "EOF"


#######################
# Token/Node Priorities
#######################
HIGHEST = 9000  # It's over 9000 -_-
ULTRA_HIGH = 4
VERY_HIGH = 3
HIGH = 2
MEDIUM = 1
LOW = 0
NO_OP = None


#############
# Token Types
#############
ASSIGNMENT_TOKEN_TYPE = "ASSIGNMENT"
COMMENT_TOKEN_TYPE = "COMMENT"
DIVIDE_TOKEN_TYPE = "DIVIDE"
GREATER_THAN_TOKEN_TYPE = "GREATER_THAN"
MINUS_TOKEN_TYPE = "MINUS"
MULTIPLY_TOKEN_TYPE = "MULTIPLY"
NUM_TOKEN_TYPE = "NUM"
NEW_LINE_TOKEN_TYPE = "NEWLINE"
PLUS_TOKEN_TYPE = "PLUS"
KEYWORD_TOKEN_TYPE = "KEYWORD"
LEFT_CURL_BRACE_TOKEN_TYPE = "LEFT_CURL_BRACE"
LEFT_PAREN_TOKEN_TYPE = "LEFT_PAREN"
RIGHT_CURL_BRACE_TOKEN_TYPE = "RIGHT_CURL_BRACE"
RIGHT_PAREN_TOKEN_TYPE = "RIGHT_PAREN"
STRING_TOKEN_TYPE = "STRING"
SPACE_TOKEN_TYPE = "SPACE"
EOL_TOKEN_TYPE = "EOL"
EOF_TOKEN_TYPE = "EOF"
VARIABLE_NAME_TOKEN_TYPE = "VARIABLE_NAME"
VARIABLE_REFERENCE_TOKEN_TYPE = "VARIABLE_REFERENCE"


##############
# Const tuples
##############
ALL_TOKENS = (
    ASSIGNMENT_TOKEN_TYPE,
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
    EOF_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    VARIABLE_REFERENCE_TOKEN_TYPE
)
CONTINUATION_TOKENS = (
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
)
IGNORE_TOKENS = (SPACE_TOKEN_TYPE,)
IGNORE_OPS = (
    SPACE_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    EOL_TOKEN_TYPE
)
FUNCTION_KEYWORDS = ("print", "main")
LOGIC_KEYWORDS = ("if", "else")
VARIABLE_KEYWORDS = ("int16",)


############
# Exceptions
############
class UnclosedParenthesisError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unclosed parenthesis in program.")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Unclosed parenthesis at {self.line_num}:{self.col_num}."


# TODO(map) Probably a chance to make the init method more DRY
# TODO(map) Because the line_num in the program starts at 0 we add 1 for now.
class InvalidTokenException(Exception):
    def __init__(self, line_num, col_num, character):
        super().__init__("Invalid token.")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.character = character

    def __str__(self):
        return f"Invalid token '{self.character}' at {self.line_num}:{self.col_num}."


class NoTerminatorError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Line is not terminted with a semicolon.")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Line {self.line_num}:{self.col_num} must end with a semicolon."


class UnknownKeywordError(Exception):
    def __init__(self, line_num, col_num, keyword):
        super().__init__("Unknown keyword")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.keyword = keyword

    def __str__(self):
        return f"Unknown keyword '{self.keyword}' at {self.line_num}:{self.col_num} in program."


class InvalidVariableNameError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid variable name")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Variable name at {self.line_num}:{self.col_num} cannot start with digit."


class KeywordMisuseException(Exception):
    def __init__(self, line_num, col_num, keyword, usage):
        super().__init__("Improper use of keyword.")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.keyword = keyword
        self.usage = usage

    def __str__(self):
        return f"Improper use of '{self.keyword}' at {self.line_num}:{self.col_num} in program. \n   Sample Usage: {self.usage}"


class UnclosedQuotationException(Exception):
    def __init__(self, line_num, col_num, string):
        super().__init__("Unclosed quotation")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.string = string

    def __str__(self):
        return f"Unclosed quotation mark for '{self.string}' at {self.line_num}:{self.col_num}."


class BadFormattedLogicBlock(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Badly formatted logic block")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Incorrectly formatted else statement at {self.line_num}:{self.col_num}. Cannot have code between if/else block."


class UnpairedElseError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unpaired else")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"else at {self.line_num}:{self.col_num} does not have a matching if block."



########
# TOKENS
########
class Token:
    def __init__(self, ttype, col, row, value, priority):
        self.ttype = ttype
        self.col = col
        self.row = row
        self.value = value
        self.priority = priority

    def __repr__(self):
        return f"[{self.ttype}, {self.row}, {self.col}, {self.value}, {self.priority}]"

    def __eq__(self, other):
        return (self.ttype == other.ttype
                and self.row == other.row
                and self.col == other.col
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
        self.child_node.parent_node = self

    def __eq__(self, other):
        child_equal = self.child_node == other.child_node
        values_equal = self.value == other.value
        return child_equal and values_equal and super().__eq__(other)

    def __repr__(self):
        return f"({self.value}({self.child_node}))"


class FunctionKeywordNode(KeywordNode):
    """
    More specialized node for Function keywords vs other types of keywords.
    """
    def __init__(self, token, value, child_node, parent_node=None):
        super().__init__(token, value, child_node, parent_node)

    def __eq__(self, other):
        return type(self) == type(other) and super().__eq__(other)


class LogicKeywordNode(KeywordNode):
    """
    More specialized node for Logic keywords vs other types of keywords.
    """
    def __init__(self, token, value, child_node, parent_node=None, true_side=None, false_side=None):
        super().__init__(token, value, child_node, parent_node)
        self.true_side = true_side
        self.false_side = false_side

        if true_side:
            for node in true_side:
                node.parent_node = self
        if false_side:
            for node in false_side:
                node.parent_node = self

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        true_side_equal = self.true_side == other.true_side
        false_side_equal = self.false_side == other.false_side
        return types_equal and true_side_equal and false_side_equal and super().__eq__(other)

    def __repr__(self):
        return f"({self.value}({self.child_node}, {self.true_side}, {self.false_side}))"


class VariableKeywordNode(KeywordNode):
    """
    More specialized node for Variable keywords vs other types of keywords.
    """
    def __init__(self, token, value, child_node, parent_node=None):
        super().__init__(token, value, child_node, parent_node)

    def __eq__(self, other):
        return type(self) == type(other) and super().__eq__(other)


class StartNode(Node):
    """
    Special node that represents the `main` keyword that starts the program.
    """
    def __init__(self, token, value, children_nodes):
        super().__init__(token, HIGHEST, None)
        self.value = value
        self.children_nodes = children_nodes
        for node in self.children_nodes:
            node.parent_node = self

    def __eq__(self, other):
        children_equal = self.children_nodes == other.children_nodes
        values_equal = self.value == other.value
        types_equal = type(self) == type(other)
        return types_equal and children_equal and values_equal and super().__eq__(other)

    def __repr__(self):
        children_nodes = "["
        for node in self.children_nodes:
            children_nodes += node.__repr__() + ","
        children_nodes += "]"
        return f"({self.value}{self.children_nodes})"


class StringNode(Node):
    """
    Node for strings in the Katana language.
    """

    def __init__(self, token, value, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value

    def __eq__(self, other):
        values_equal = self.value == other.value
        return values_equal and super().__eq__(other)

    def __repr__(self):
        return f"'{self.value}'"


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


class AssignmentNode(ExpressionNode):
    """
    Node for assigning values to variables. The left side is always the
    variable with the right side being the value.
    """

    def __init__(self, token, value, left_side=None, right_side=None, parent_node=None):
        super().__init__(token, value, MEDIUM, left_side, right_side, parent_node)


    def __eq__(self, other):
        types_equal = type(self) == type(other)
        if not types_equal:
            assert False, f"Type {type(self)} != {type(other)}"
        return (types_equal and
                super().__eq__(other))



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


class CompareNode(ExpressionNode):
    """
    Node specific for doing comparison
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


class VariableNode(Node):
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


class VariableReferenceNode(Node):
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



#########
# PROGRAM
#########
class Program:
    """
    Helper class to track relevant information on the program that is being
    compiled.
    """

    def __init__(self, lines):
        self.lines = lines
        self.curr_col = -1
        self.curr_line = 0
        self.curr_line_len = len(lines[0])
        self.line_count = len(lines)
        self.end_pos = sum(len(line) for line in lines)

    def advance_line(self):
        self.curr_col = -1
        self.curr_line += 1
        if self.has_next_line():
            self.curr_line_len = len(self.get_curr_line())

    def advance_character(self):
        self.curr_col += 1

    def get_curr_char(self):
        return self.lines[self.curr_line][self.curr_col]

    def get_next_char(self):
        return self.lines[self.curr_line][self.curr_col + 1]

    def has_next_char(self):
        return self.curr_col + 1 < self.curr_line_len

    def get_curr_line(self):
        return self.lines[self.curr_line]

    def get_next_line(self):
        return self.lines[self.curr_line + 1]

    def has_next_line(self):
        return self.curr_line + 1 < self.line_count + 1


########
# UTILS
########
def print_verbose_message(message):
    if verbose_flag:
        print(message)


def print_exception_message(program, position, exception):
    print(program)
    print(" "*position + "^")
    print(exception)


#######
# LEXER
#######
class Lexer:
    def __init__(self, program):
        self.program = program
        self.token_list = []
        self.left_paren_idx_list = []
        self.right_paren_idx_list = []
        self.if_idx_list = []
        self.else_idx_list = []
        self.variable_name_list = []
        self.unpaired_parens = 0
        self.misused_keywords = 0
        self.comment_index = -1

    def lex(self):
        paren_error_row = 0
        paren_error_col = 0
        while self.program.has_next_char() and self.program.has_next_line():
            self.program.advance_character()
            self.update_comment_index()

            # There is only a comment on this line and nothing else.
            if self.comment_index == 0:
                if self.comment_index == 0:
                    token = Token(COMMENT_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, self.program.get_curr_line()[:-1], LOW)
                    if token.ttype not in IGNORE_TOKENS:
                        self.token_list.append(token)
                    token = Token(NEW_LINE_TOKEN_TYPE, len(self.program.get_curr_line()) - 1, self.program.curr_line, self.program.get_curr_line()[-1:], LOW)
                    if token.ttype not in IGNORE_TOKENS:
                        self.token_list.append(token)
                    self.program.advance_line()
                    self.comment_index = -1
            elif self.comment_index > 0 and self.program.curr_col == self.comment_index:
                token = Token(COMMENT_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, self.program.get_curr_line()[self.comment_index:-1], LOW)
                if token.ttype not in IGNORE_TOKENS:
                    self.token_list.append(token)
                token = Token(NEW_LINE_TOKEN_TYPE, len(self.program.get_curr_line()) - 1, self.program.curr_line, self.program.get_curr_line()[-1:], LOW)
                if token.ttype not in IGNORE_TOKENS:
                    self.token_list.append(token)
                self.program.advance_line()
                self.comment_index = -1
            else:
                token = self.generate_token(self.program.get_curr_char())
                # Advance the line if we have an EOL token
                if token.ttype == NEW_LINE_TOKEN_TYPE:
                    self.program.advance_line()
                    self.comment_index = -1
                else:
                    if token.ttype == NUM_TOKEN_TYPE:
                        while self.program.get_next_char().isnumeric():
                            token.value += self.program.get_next_char()
                            self.program.curr_col += 1
                    elif token.ttype == LEFT_PAREN_TOKEN_TYPE:
                        self.unpaired_parens += 1
                        self.left_paren_idx_list.append(len(self.token_list))
                    elif token.ttype == RIGHT_PAREN_TOKEN_TYPE:
                        self.unpaired_parens -= 1
                        self.right_paren_idx_list.append(len(self.token_list))
                if token.ttype not in IGNORE_TOKENS:
                    self.token_list.append(token)

        # Always add end of file token to list
        self.token_list.append(Token(EOF_TOKEN_TYPE, 0, self.program.curr_line, EOF, LOW))

        if len(self.left_paren_idx_list) != len(self.right_paren_idx_list):
            for token in self.token_list:
                if token.ttype == LEFT_PAREN_TOKEN_TYPE:
                    self.unpaired_parens += 1
                    paren_error_row = token.row
                    paren_error_col = token.col
                elif token.ttype == RIGHT_PAREN_TOKEN_TYPE:
                    self.unpaired_parens -= 1
                    paren_error_row = token.row
                    paren_error_col = token.col

            if self.unpaired_parens != 0:
                upe = UnclosedParenthesisError(paren_error_row, paren_error_col)
                self.print_invalid_character_error(self.program, paren_error_col, paren_error_row)
                print(upe)
                raise upe

        # TODO(map) Make this more robust as a method by itself.
        if len(self.else_idx_list) > 0:
            # TODO(map) This isn't great as it assumes the last else is the problem.
            if len(self.if_idx_list) < len(self.else_idx_list):
                err_token = self.token_list[self.else_idx_list[-1]]
                raise UnpairedElseError(err_token.row, err_token.col)
            for idx in reversed(self.else_idx_list):
                token_list = self.token_list[:idx]
                if token_list[idx - 2].ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                    bad_token = token_list[idx - 3]
                    raise BadFormattedLogicBlock(bad_token.row, 0)

        return self.token_list

    def update_comment_index(self):
        if "//" in self.program.get_curr_line():
            self.comment_index = self.program.get_curr_line().index("//")

    def get_single_line_comment_token(self) -> Token:
        end_of_comment_pos = self.program.get_curr_line()[self.program.curr_col:].index(
            "\n") + self.program.curr_col
        token = Token(COMMENT_TOKEN_TYPE, self.program.curr_col, self.program.curr_line,
                      self.program.get_curr_line()[self.program.curr_col:end_of_comment_pos], LOW)
        self.program.curr_col = end_of_comment_pos
        return token

    def generate_token(self, character) -> Token:
        try:
            if character.isnumeric():
                if len(self.token_list) > 0 and not self.token_list[-1].ttype != KEYWORD_TOKEN_TYPE:
                    raise InvalidVariableNameError(self.program.curr_line, self.program.curr_col)
                else:
                    return Token(NUM_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character == '+':
                return Token(PLUS_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, MEDIUM)
            elif character == '-':
                return Token(MINUS_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, MEDIUM)
            elif character == '*':
                return Token(MULTIPLY_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '/':
                return Token(DIVIDE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '=':
                return Token(ASSIGNMENT_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '>':
                return Token(GREATER_THAN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '{':
                return Token(LEFT_CURL_BRACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == '(':
                return Token(LEFT_PAREN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == '}':
                return Token(RIGHT_CURL_BRACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == ')':
                self.check_for_valid_termination(character)
                return Token(RIGHT_PAREN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == ';':
                return Token(EOL_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character == '"':
                return self.generate_string_token()
            elif character.isalpha():
                return self.generate_keyword_token()
            elif character == "\n":
                self.check_for_valid_termination(character)
                return Token(NEW_LINE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character.isspace():  # Never care about spaces
                return Token(SPACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            else:
                raise InvalidTokenException(self.program.curr_line, self.program.curr_col, character)
        except InvalidVariableNameError as ivne:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(ivne)
            raise ivne
        except NoTerminatorError as nte:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(nte)
            raise nte
        except InvalidTokenException as ite:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(ite)
            raise ite
        except UnknownKeywordError as uke:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(uke)
            raise uke
        except UnclosedQuotationException as uqe:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(uqe)
            raise uqe

    def print_invalid_character_error(self, program, col, row):
        print(program.lines[row])
        print(" "*col + "^")

    def check_for_valid_termination(self, value):
        if value == "\n":
            is_previous_token_continuation_type = self.token_list[len(self.token_list) - 1].ttype in CONTINUATION_TOKENS
            is_previous_token_eol = self.token_list[len(self.token_list) - 1].ttype == EOL_TOKEN_TYPE
            # TODO(map) Should I check to make sure there is not a semicolon?
            if not is_previous_token_continuation_type and not is_previous_token_eol:
                raise NoTerminatorError(self.program.curr_line, self.program.curr_col)
            elif is_previous_token_continuation_type or is_previous_token_eol:
                pass
            else:
                assert False, "Don't know how to handle new line termination."
        elif value == ")":
            if len(self.left_paren_idx_list) > 0:
                terminator_present = self.program.get_next_char() == ";"
                left_paren_first_token = self.token_list[self.left_paren_idx_list[-1]].col == 0
                left_paren_first_token_after_spaces = self.token_list[self.left_paren_idx_list[-1]].row != self.token_list[self.left_paren_idx_list[-1] - 1].row
                left_paren_first = left_paren_first_token or left_paren_first_token_after_spaces
                # Get the token before the left paren.
                token = self.token_list[self.left_paren_idx_list[-1] - 1]
                left_paren_has_keyword = token.value in LOGIC_KEYWORDS or token.value == "main"
                if not terminator_present and not left_paren_first and not left_paren_has_keyword:
                    raise NoTerminatorError(self.program.curr_line, self.program.curr_col + 1)
        else:
            assert False, "Invalid scenario to check for termination."

    def generate_keyword_token(self):
        keyword = ""
        original_pos = self.program.curr_col
        while self.program.get_curr_char().isalpha() or self.program.get_curr_char().isnumeric():
            keyword += self.program.get_curr_char()
            # TODO(map) De-couple the advance from generating the token
            self.program.curr_col += 1

        # TODO(map) This is a dirty hack and will be resolved when I decouple
        # the problem in the TODO above.
        self.program.curr_col -= 1
        if keyword in FUNCTION_KEYWORDS + VARIABLE_KEYWORDS + LOGIC_KEYWORDS:
            if keyword == "if":
                self.if_idx_list.append(len(self.token_list))
            elif keyword == "else":
                self.else_idx_list.append(len(self.token_list))
            return Token(KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, ULTRA_HIGH)
        elif len(self.token_list) > 0 and self.token_list[-1].value in VARIABLE_KEYWORDS:
            self.variable_name_list.append(keyword)
            return Token(VARIABLE_NAME_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif keyword in self.variable_name_list:
            return Token(VARIABLE_REFERENCE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        else:
            raise UnknownKeywordError(self.program.curr_line, original_pos, keyword)

    def generate_string_token(self):
        string = ""
        original_pos = self.program.curr_col
        self.program.curr_col += 1

        while self.program.get_curr_char() != '"':
            if self.program.get_curr_char() == ";" or self.program.get_curr_char() == "\n":
                raise UnclosedQuotationException(self.program.curr_line, self.program.curr_col, string)
            string += self.program.get_curr_char()
            self.program.curr_col += 1

        return Token(STRING_TOKEN_TYPE, original_pos, self.program.curr_line, string, LOW)


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
        try:
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
            elif self.curr_token.ttype == ASSIGNMENT_TOKEN_TYPE:
                node = self.parse_op(AssignmentNode, root_node)
            elif self.curr_token.ttype == GREATER_THAN_TOKEN_TYPE:
                node = self.parse_op(CompareNode, root_node)
            elif self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
                node = self.handle_parenthesis()
            elif self.curr_token.ttype == LEFT_CURL_BRACE_TOKEN_TYPE:
                node = NoOpNode(self.curr_token)
            elif self.curr_token.ttype == RIGHT_CURL_BRACE_TOKEN_TYPE:
                node = NoOpNode(self.curr_token)
            elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE:
                node = self.handle_keyword()
            elif self.curr_token.ttype == STRING_TOKEN_TYPE:
                node = self.handle_string()
            elif self.curr_token.ttype == VARIABLE_NAME_TOKEN_TYPE:
                node = VariableNode(self.curr_token, self.curr_token.value, None)
            elif self.curr_token.ttype == VARIABLE_REFERENCE_TOKEN_TYPE:
                node = VariableReferenceNode(self.curr_token, self.curr_token.value, None)
            elif self.curr_token.ttype in IGNORE_OPS:
                node = NoOpNode(self.curr_token)
            elif self.curr_token.ttype == EOF_TOKEN_TYPE:
                node = NoOpNode(self.curr_token)
                self.has_next_token = False
            else:
                assert False, f"Unknown token type {self.curr_token.ttype}"
            return node
        except KeywordMisuseException as kme:
            print_exception_message(("\n").join(program_lines), kme.col_num, kme)

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
                type(root_node) not in [LiteralNode, VariableNode, VariableReferenceNode]
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

    def handle_string(self):
        return StringNode(self.curr_token, self.curr_token.value, None)

    def handle_keyword(self):
        node_value = self.curr_token.value

        # TODO(map) Move the methods to a map based on the keyword.
        if node_value == "print":
            keyword_token = self.curr_token
            # Move past keyword token
            self.advance_token()
            contents = self.handle_print_keyword(keyword_token)
            keyword_node = FunctionKeywordNode(keyword_token, keyword_token.value, contents, None)
        elif node_value == "main":
            keyword_token = self.curr_token
            # Move past keyword token
            self.advance_token()
            children_nodes = self.handle_main_keyword(keyword_token)
            keyword_node = StartNode(keyword_token, keyword_token.value, children_nodes)
        elif node_value == "int16":
            keyword_token = self.curr_token
            # Move past keyword token
            self.advance_token()

            child_node = None
            while self.curr_token.ttype != EOL_TOKEN_TYPE:
                child_node = self.process_token(child_node)
                self.advance_token()
            keyword_node = VariableKeywordNode(keyword_token, keyword_token.value, child_node, None)
        elif node_value == "if":
            keyword_token = self.curr_token
            truth_body = None
            false_body = None
            # Move past keyword token
            self.advance_token()

            # TODO(map) Should I just call handle_parenthesis here?
            # Move past paren token
            self.advance_token()

            # Get the comparison within the parens.
            paren_contents = None
            while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
                paren_contents = self.process_token(paren_contents)
                self.advance_token()

            # Move past closing paren on conditional check
            self.advance_token()

            # Move past left curl bracket
            self.advance_token()

            truth_node_list = []
            while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                ret_node = self.process_token(truth_body)
                if type(ret_node) != NoOpNode:
                    # TODO(map) This only allows for a single line of code to
                    # be in the body. It will fail if there are two lines of
                    # code.
                    truth_body = ret_node
                self.advance_token()
                if self.curr_token.ttype == EOL_TOKEN_TYPE:
                    truth_node_list.append(truth_body)
                    truth_body = None

            # Move past the right curl brace to close the if body.
            self.advance_token()

            # TODO(map) Handle multiple return characters between if and else.
            # Move past the new line after the curl bracket if present.
            if self.curr_token.ttype == NEW_LINE_TOKEN_TYPE:
                self.advance_token()

            # Flag if there is an else keyword and parse it.
            is_else_keyword_present = self.curr_token.value == "else"
            false_node_list = []
            if is_else_keyword_present:
                # Move past the else keyword.
                self.advance_token()

                # Move past the curl bracket that starts the else body.
                self.advance_token()

                while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                    ret_node = self.process_token(false_body)
                    if type(ret_node) != NoOpNode:
                        # TODO(map) This only allows for a single line of code 
                        # to be in the body. It will fail if there are two 
                        # lines of code.
                        false_body = self.process_token(false_body)
                    self.advance_token()
            else:
                # TODO(map) This is not clean. Find a better way to determine
                # if there is an else without actually advancing the token.

                self.curr_token_pos -= 1
                self.curr_token = self.token_list[self.curr_token_pos]

            return LogicKeywordNode(keyword_token, keyword_token.value, paren_contents, true_side=truth_node_list, false_side=false_node_list)
        else:
            assert False, f"Keyword {node_value} not implemented"

        return keyword_node

    def handle_print_keyword(self, keyword_token):
        """Signature is `print(VALUE)`"""
        # Confirm the left paren is right after print keyword
        if not self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, "print(VALUE): prints the VALUE to the screen")

        # Move past the left paren.
        self.advance_token()

        # Case where `print` was called with nothing to print.
        if self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, "print(VALUE);: prints the VALUE to the screen")

        # Parse the inner parts of the print function
        root_node = None
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
            root_node = self.process_token(root_node)
            self.advance_token()
        return root_node

    def handle_main_keyword(self, keyword_token):
        """Signature is `main() { BODY };`"""
        # Confirm the left paren is right after the main keyword
        if not self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, "main() { BODY; };: Executes the BODY of code within the main method.")

        # Move past the left paren.
        self.advance_token()

        # Confirm the right paren closes the left.
        if not self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, "main() { BODY; };: Executes the BODY of code within the main method.")

        # Move pas the right paren
        self.advance_token()

        # Confirm left curl brack is present.
        if not self.curr_token.ttype == LEFT_CURL_BRACE_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, "main() { BODY; };: Executes the BODY of code within the main method.")

        # Move past the left curl brace
        self.advance_token()

        node_list = []
        # Parse the body.
        root_node = None
        while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
            node = self.process_token(root_node)
            if node and type(node) != NoOpNode:
                root_node = node
            if self.curr_token.ttype == EOL_TOKEN_TYPE:
                node_list.append(root_node)
                root_node = None
            elif type(node) ==  LogicKeywordNode and node.value == "if":
                node_list.append(root_node)
                root_node = None
            self.advance_token()
        return node_list


##########
# Compiler
##########
class Compiler:

    def __init__(self, ast):
        self.ast = ast
        self.output_path = os.getcwd() + "/out.asm"
        self.string_count = 0
        self.var_count = 0
        self.raw_strings = {}
        self.variables = {}

    def compile(self):
        self.create_empty_out_file()
        # Declare the global start only.
        self.create_global_start()
        # Set up the keyword built in functions
        self.create_keyword_functions()
        # Write the program
        self.write_assembly()
        self.create_assembly_for_exit()

    def create_empty_out_file(self):
        with open(self.output_path, 'w') as compiled_program:
            compiled_program.write(";; Start of program\n")

    def create_start_point(self, compiled_program):
        compiled_program.write("section .text\n")
        compiled_program.write("    _start:\n")

    def get_assembly(self):
        asm = []
        for node in self.ast.children_nodes:
            asm.extend(self.traverse_tree(node))
        return asm

    def write_assembly(self):
        with open(self.output_path, 'a') as compiled_program:
            asm = self.get_assembly()
            # Write any raw strings that will be used that aren't assigned to a
            # variable in the code.
            for key in self.raw_strings:
                for line in self.raw_strings[key]:
                    compiled_program.write(line)
            # Write the variables first, them move to assembly.
            for key in self.variables:
                # Write the assembly for the string.
                for line in self.variables[key]["asm"]:
                    compiled_program.write(line)
            self.create_start_point(compiled_program)
            for line in asm:
                compiled_program.write(line)

    def traverse_tree(self, node):
        if isinstance(node, StartNode):
            return []
        elif isinstance(node, ExpressionNode):
            if node.left_side and not node.left_side.visited:
                print_verbose_message(
                    f"Traversing from {node} to left side node {node.left_side}")
                return self.traverse_tree(node.left_side)
            elif node.right_side and not node.right_side.visited:
                print_verbose_message(
                    f"Traversing from {node} to right side node {node.right_side}")
                return self.traverse_tree(node.right_side)
            else:
                node.visited = True
                if node.parent_node:
                    return self.process_op_node(node) + self.traverse_tree(node.parent_node)
                else:
                    return self.process_op_node(node)
        elif isinstance(node, LiteralNode):
            node.visited = True
            if node.parent_node:
                return self.get_push_number_onto_stack_asm(node.value) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_number_onto_stack_asm(node.value)
        elif isinstance(node, FunctionKeywordNode):
            if node.child_node and not node.child_node.visited:
                return self.traverse_tree(node.child_node)
            elif node.parent_node:
                node.visited = True
                return self.get_keyword_asm() + self.traverse_tree(node.parent_node)
            else:
                node.visted = True
                return self.get_keyword_asm()
        elif isinstance(node, VariableKeywordNode):
            if node.child_node and not node.child_node.visited:
                return self.traverse_tree(node.child_node)
            elif node.parent_node:
                node.visited = True
                return self.traverse_tree(node.parent_node)
            else:
                node.visted = True
                return []
        elif isinstance(node, StringNode):
            self.string_count += 1
            node.visited = True
            key = f"string_{self.string_count}"
            self.raw_strings[key] = self.get_string_asm(node.value, len(node.value), self.string_count)
            if node.parent_node:
                return self.get_push_string_asm(self.string_count, len(node.value)) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_string_asm(self.string_count, len(node.value))
        elif isinstance(node, VariableNode):
            self.var_count += 1
            node.visited = True
            section_text = f"var_{self.var_count}"
            # Go to the right side of the assignment expression, mark the node
            # as visited so we don't push onto the stack since we are just
            # assigning, and pass that value to the variable declaration.
            value_node = node.parent_node.right_side
            print_verbose_message(f"Traversing from {node.parent_node} to right side node {value_node}")
            value_node.visited = True
            # TODO(map) This uses `number` which is bad when new vars arrive.
            self.variables[node.value] = {
                "section":  section_text,
                "var_name": f"number_{self.var_count}",
                "asm": self.get_assignment_asm(self.var_count, value_node.value)
            }
            return self.traverse_tree(node.parent_node)
        elif isinstance(node, VariableReferenceNode):
            node.visited = True
            var_ref = self.variables[node.value]["var_name"]
            return self.get_push_var_onto_stack_asm(var_ref) + self.traverse_tree(node.parent_node)
        elif isinstance(node, LogicKeywordNode):
            node.visited = True
            if not node.child_node.visited:
                return self.traverse_tree(node.child_node)
            for true_node in node.true_side:
                if not true_node.visited:
                    return self.traverse_tree(true_node)
            if node.false_side and not node.false_side.isempty():
                for false_node in node.false_side:
                    if not false_node.visited:
                        return self.traverse_tree(false_node)
            if not node.false_side or node.false_side.isempty():
                return self.get_false_side_asm() + self.get_push_number_onto_stack_asm(0)
        else:
            assert False, (f"This node type {type(node)} is not yet implemented.")

    def process_op_node(self, node):
        if node.value == "+":
            return self.get_add_asm()
        elif node.value == "-":
            return self.get_sub_asm()
        elif node.value == "*":
            return self.get_mul_asm()
        elif node.value == "/":
            return self.get_div_asm()
        elif node.value == ">":
            return self.get_conditional_greater_than_asm()
        elif node.value == "=":
            # We don't actually need to do any ops for this node right now.
            return []
        else:
            assert False, f"Unrecognized root node value {node.value}"

    def create_keyword_functions(self):
        # TODO(map) This doesn't work for numbers above 9
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    print:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get variable value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Check if this is a number\n")
            compiled_program.write("        cmp rax, 10\n")
            compiled_program.write("        jl number\n")
            compiled_program.write("        jge str\n")
            compiled_program.write("    ;; If number add 48 to print\n")
            compiled_program.write("    number:\n")
            compiled_program.write("        add rax, 48\n")
            compiled_program.write("        push rax\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        jmp finish\n")
            compiled_program.write("   ;; If string get the value\n")
            compiled_program.write("   str:\n")
            compiled_program.write("        ;; Get variable length\n")
            compiled_program.write("        pop rdx\n")
            compiled_program.write("        mov rsi, rax\n")
            compiled_program.write("   ;; Finish the print\n")
            compiled_program.write("   finish:\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")

    def create_global_start(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    global _start\n")

    def get_push_number_onto_stack_asm(self, num):
        return [f"    push {num}\n"]

    def get_push_var_onto_stack_asm(self, val):
        return [f"    push qword [{val}]\n"]

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

    def get_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call print\n"
        ]

    def get_true_side_asm(self):
        return [
            "    greater:\n",
        ]

    def get_false_side_asm(self):
        return [
            "    less:\n",
        ]

    def get_conditional_greater_than_asm(self):
        return [
            "    pop rax\n",
            "    pop rbx\n",
            "    cmp rbx, rax\n",
            "    jg greater\n",
            "    jle less\n",
            "    greater:\n"
        ]

    def get_string_asm(self, string, string_length, string_count):
        return [
            f"section .string_{string_count}\n",
            f"    string_{string_count} db '{string}', {string_length}\n",
            f"    len_{string_count} equ $ - string_{string_count}\n"
        ]

    def get_push_string_asm(self, string_count, string_length):
        return [
            f"    push {string_length}\n",
            f"    push string_{string_count}\n",
        ]

    def get_assignment_asm(self, var_count, value):
        return [
            f"section .var_{var_count}\n",
            f"    number_{var_count} dq {value}\n"
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
program_lines = None
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--program", help="The program that should be parse.")
    arg_parser.add_argument("--verbose", action="store_true",
                            help="Adds verbosity output to the steps.")
    arg_parser.add_argument("--lex", action="store_true",
                            help="Lex the program and return a token list.")
    arg_parser.add_argument("--parse", action="store_true",
                            help="Return the program and print the AST.")
    arg_parser.add_argument("--compile", action="store_true",
                            help="Compile the program and create assembly.")
    arg_parser.add_argument("--run", action="store_true",
                            help="Run the assembled program.")
    args = arg_parser.parse_args()

    verbose_flag = args.verbose
    with open(args.program, 'r') as code:
        token_list = None
        ast = None
        if args.lex or args.parse or args.compile or args.run:
            program = Program(code.readlines())
            program_lines = program.lines
            lexer = Lexer(program)
            token_list = lexer.lex()
            print_verbose_message(token_list)
        if args.parse or args.compile or args.run:
            parser = Parser(token_list)
            ast = parser.parse()
            print_verbose_message(ast)
        if args.compile or args.run:
            compiler = Compiler(ast)
            compiler.compile()
        if args.run:
            run_program()
