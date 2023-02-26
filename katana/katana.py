import argparse
import os
# TODO(map) Move all the classes and enums outs so imports are nice
#########
# GLOBALS
#########
verbose_flag = False
raise_assertion_flag = True

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
BOOLEAN_TOKEN_TYPE = "BOOLEAN"
CHARACTER_TOKEN_TYPE = "CHARACTER"
COMMA_TOKEN_TYPE = "COMMA"
COMMENT_TOKEN_TYPE = "COMMENT"
DIVIDE_TOKEN_TYPE = "DIVIDE"
EQUAL_TOKEN_TYPE = "EQUAL"
GREATER_THAN_TOKEN_TYPE = "GREATER_THAN"
MINUS_TOKEN_TYPE = "MINUS"
MULTIPLY_TOKEN_TYPE = "MULTIPLY"
NUM_TOKEN_TYPE = "NUM"
NEW_LINE_TOKEN_TYPE = "NEWLINE"
PLUS_TOKEN_TYPE = "PLUS"
KEYWORD_TOKEN_TYPE = "KEYWORD"
LEFT_CURL_BRACE_TOKEN_TYPE = "LEFT_CURL_BRACE"
LEFT_PAREN_TOKEN_TYPE = "LEFT_PAREN"
LESS_THAN_TOKEN_TYPE = "LESS_THAN"
RANGE_INDICATION_TOKEN_TYPE = "RANGE"
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
    EOL_TOKEN_TYPE,
    EOF_TOKEN_TYPE,
    KEYWORD_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    MINUS_TOKEN_TYPE,
    MULTIPLY_TOKEN_TYPE,
    NUM_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    PLUS_TOKEN_TYPE,
    RIGHT_PAREN_TOKEN_TYPE,
    SPACE_TOKEN_TYPE,
    VARIABLE_NAME_TOKEN_TYPE,
    VARIABLE_REFERENCE_TOKEN_TYPE
)
CONTINUATION_TOKENS = (
    LEFT_CURL_BRACE_TOKEN_TYPE,
    LEFT_PAREN_TOKEN_TYPE,
    RIGHT_CURL_BRACE_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE
)
IGNORE_TOKENS = (SPACE_TOKEN_TYPE,)
IGNORE_OPS = (
    SPACE_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
    EOL_TOKEN_TYPE
)
FUNCTION_KEYWORDS = ("print", "printl", "main", "charAt")
LOGIC_KEYWORDS = ("if", "else", "loopUp", "loopDown", "loopFrom")
# TODO(map) Change this to int until we set up 32 bit mode.
VARIABLE_KEYWORDS = ("const", "int16", "string", "bool", "char")


###################
# Method Signatures
###################
CHAR_AT_SIGNATURE = "charAt(STRING, INDEX): extracts the character at INDEX from the STRING"
MAIN_SIGNATURE = "main() { BODY; };: Executes the BODY of code within the main method."
PRINT_SIGNATURE = "print(VALUE);: prints the VALUE to the screen"
LOOP_UP_SIGNATURE = "loopUp(VALUE) { BODY; }: Loops from 0 to VALUE executing BODY each time"
LOOP_DOWN_SIGNATURE = "loopDown(VALUE) { BODY; }: Loops from VALUE to 0 executing BODY each time"
LOOP_FROM_SIGNATURE = "loopFrom(START..END) { BODY; }: Loops from START to END executing BODY each time"


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


class InvalidCharException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid char")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Invalid declaration of `char` at {self.line_num}:{self.col_num}."


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


class InvalidTypeDeclarationException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid type")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Invalid type at {self.line_num}:{self.col_num}."


class InvalidAssignmentException(Exception):
    def __init__(self, line_num, col_num, base_type, assignment_type):
        super().__init__("Invalid assignment")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.base_type = base_type
        self.assignment_type = assignment_type

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot assign a {self.base_type} with a {self.assignment_type}."


class InvalidConcatenationException(Exception):
    def __init__(self, line_num, col_num, base_type, concat_type):
        super().__init__("Invalid concatenation")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.base_type = base_type
        self.concat_type = concat_type

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot concatenate a {self.base_type} with a {self.concat_type}."


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
        if not priority_equal and raise_assertion_flag:
            assert False, f"{self} priority {self.priority} != {other} priority {other.priority}."

        token_equal = self.token == other.token
        if not token_equal and raise_assertion_flag:
            assert False, f"Tokens {self.token} != {other.token}"

        return priority_equal and token_equal

    def can_traverse_to_parent(self):
        if self.parent_node:
            return type(self.parent_node) != LogicKeywordNode and type(self.parent_node) != FunctionKeywordNode
        else:
            return False


class NoOpNode(Node):
    """
    Node that functionally does nothing. This is in case I want to preserve
    data across the compilation much like with useless tokens.
    """
    def __init__(self,
                 token: Token) -> None:
        self.token: Token = token
        super().__init__(token, NO_OP, None)


class ArgSeparatorNode(NoOpNode):
    """
    Node to declare a type we can use for conditional checks. Child of NoOp as
    we don't want to do anything with it, but it is specific for separating out
    arguments in a function.
    """
    def __init__(self, token):
        super().__init__(token)


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


class FunctionNode(Node):
    """
    Node for all things function based. Key difference between this and keyword
    node is that the function node has a list of args but a keyword only has
    a single childe node.
    """
    def __init__(self, token, value, arg_nodes, parent_node=None):
        super().__init__(token, ULTRA_HIGH, parent_node)
        self.value = value
        self.arg_nodes = arg_nodes
        for node in arg_nodes:
            node.parent_node = self

    def __eq__(self, other):
        args_equal = self.arg_nodes == other.arg_nodes
        return args_equal and type(self) == type(other) and super().__eq__(other)

    def __repr__(self):
        arg_nodes = "["
        for node in self.arg_nodes:
            arg_nodes += node.__repr__() + ","
        arg_nodes += "]"
        return f"({self.value}{arg_nodes})"


class FunctionKeywordNode(FunctionNode):
    """
    More specialized node for Function keywords vs other types of keywords.
    """
    def __init__(self, token, value, arg_nodes, parent_node=None):
        super().__init__(token, value, arg_nodes, parent_node)

    def __eq__(self, other):
        return type(self) == type(other) and super().__eq__(other)


class LogicKeywordNode(KeywordNode):
    """
    More specialized node for Logic keywords vs other types of keywords.
    """
    def __init__(self, token, value, child_node, parent_node=None, true_side=[], false_side=[]):
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


class LoopKeywordNode(KeywordNode):
    """
    Specialized node for the different types of loops that exist.
    """
    def __init__(self, token, value, child_node, parent_node=None, loop_body=[]):
        super().__init__(token, value, child_node, parent_node)
        self.loop_body = loop_body

        if loop_body:
            for node in loop_body:
                node.parent_node = self

    def __hash__(self):
        return hash(f"{self.__repr__()}_{self.token.row}_{self.token.col}")

    def __repr__(self):
        return f"({self.value}({self.child_node}, {self.loop_body}))"


class LoopUpKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `loopUp` keyword specifically.
    """
    def __init__(self, token, value, child_node, parent_node=None, loop_body=[]):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        self.start_value = 0
        self.end_value = child_node.value

        if loop_body:
            for node in loop_body:
                node.parent_node = self

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        loop_body_equal = self.loop_body == other.loop_body
        return types_equal and loop_body_equal and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class LoopDownKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `loopDown` keyword specifically.
    """
    def __init__(self, token, value, child_node, parent_node=None, loop_body=[]):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        self.start_value = child_node.value
        self.end_value = 0

        if loop_body:
            for node in loop_body:
                node.parent_node = self

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        loop_body_equal = self.loop_body == other.loop_body
        return types_equal and loop_body_equal and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class LoopFromKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `loopFrom` keyword specifically.
    """
    def __init__(self, token, value, child_node, parent_node=None, loop_body=[]):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        self.start_value = child_node.left_side.value
        self.end_value = child_node.right_side.value

        if loop_body:
            for node in loop_body:
                node.parent_node = self

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        loop_body_equal = self.loop_body == other.loop_body
        return types_equal and loop_body_equal and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


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


class CharNode(Node):
    """
    Node for chars in the Katana language.
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
        if self.parent_node and not other.parent_node and raise_assertion_flag:
            assert False, (f"Found parent node on self {self} but not other {other}")
        elif not self.parent_node and other.parent_node and raise_assertion_flag:
            assert False, (f"Found parent node on other {other} but not self {self}")
        elif not self.parent_node and not other.parent_node:
            parents_equal = True
        else:
            parents_equal = (self.parent_node and other.parent_node
                             and self.parent_node.token == other.parent_node.token
                             and self.parent_node.priority == other.parent_node.priority)

        left_side_equal = self.left_side == other.left_side
        right_side_equal = self.right_side == other.right_side
        if not left_side_equal and raise_assertion_flag:
            assert False, "Left sides were not equal."
        elif not right_side_equal and raise_assertion_flag:
            assert False, "Right sides were not equal."
        elif not parents_equal and raise_assertion_flag:
            assert False, "Parents were not equal"

        types_equal = type(self) == type(other)
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"

        values_equal = self.value == other.value
        if not values_equal and raise_assertion_flag:
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
        if not types_equal and raise_assertion_flag:
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
        if not types_equal and raise_assertion_flag:
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
        if not types_equal and raise_assertion_flag:
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
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        return (types_equal and
                super().__eq__(other))

    def __hash__(self):
        return hash(f"{self.__repr__()}_{self.token.row}_{self.token.col}")

    def can_traverse_to_parent(self):
        if self.parent_node:
            return True
        else:
            return False


class RangeNode(ExpressionNode):
    """
    Node specific for setting up a range to loop over.
    """
    def __init__(self, token, value, left_side=None, right_side=None,
                 parent_node=None):
        super().__init__(token, value, MEDIUM, left_side, right_side,
                         parent_node)

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        return (types_equal and
                super().__eq__(other))

    def __hash__(self):
        return hash(f"{self.__repr__()}_{self.token.row}_{self.token.col}")


class NumberNode(Node):
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
            assert False, f"Value {self.value} != {other.value}"
        return (types_equal and values_equal)

    def __repr__(self):
        return f"{self.value}"


class BooleanNode(Node):
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
            assert False, f"Value {self.value} != {other.value}"
        return (types_equal and values_equal)

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash(f"{self.__repr__()}_{self.token.row}_{self.token.col}")


class VariableNode(Node):
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
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
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
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

        # Do checking to make sure the tokens make sense to be parsed.
        self.check_paren_pairing()
        self.check_if_else_blocks()

        # Return the list of tokens but filter out any NEW_LINE_TOKEN_TYPE as
        # they don't serve a value in the parser. Don't modify the original
        # so that it can be viewed if desired for debugging.
        return list(filter(lambda token: (token.ttype != NEW_LINE_TOKEN_TYPE), self.token_list))

    def update_comment_index(self):
        if "//" in self.program.get_curr_line():
            self.comment_index = self.program.get_curr_line().index("//")

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
            elif character == '=' and self.program.get_next_char() != '=':
                return Token(ASSIGNMENT_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '=' and self.program.get_next_char() == '=':
                return self.handle_equal_operator()
            elif character == '>':
                return Token(GREATER_THAN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
            elif character == '<':
                return Token(LESS_THAN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, HIGH)
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
            elif character == '\'':
                return self.generate_char_token()
            elif character == '"':
                return self.generate_string_token()
            elif character == ".":
                return self.handle_dot_character()
            elif character == ",":
                return Token(COMMA_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
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
        except InvalidCharException as ice:
            self.print_invalid_character_error(self.program, self.program.curr_col, self.program.curr_line)
            print(ice)
            raise ice

    def print_invalid_character_error(self, program, col, row):
        print(program.lines[row])
        print(" "*col + "^")

    def check_for_valid_termination(self, value):
        if value == "\n":
            is_previous_token_continuation_type = self.token_list[len(self.token_list) - 1].ttype in CONTINUATION_TOKENS
            is_previous_token_eol = self.token_list[len(self.token_list) - 1].ttype == EOL_TOKEN_TYPE
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
        # Set the keyword to the first character and mark the position in the
        # program.
        keyword = self.program.get_curr_char()
        original_pos = self.program.curr_col

        # Loop while the next char is alphanumeric.
        while self.program.get_next_char().isalpha() or self.program.get_next_char().isnumeric():
            self.program.advance_character()
            keyword += self.program.get_curr_char()

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
        elif keyword in ["true", "false"]:
            return Token(BOOLEAN_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        else:
            raise UnknownKeywordError(self.program.curr_line, original_pos, keyword)

    def generate_string_token(self):
        string = ""
        original_pos = self.program.curr_col
        self.program.advance_character()

        while self.program.get_curr_char() != '"':
            if self.program.get_curr_char() == ";" or self.program.get_curr_char() == "\n":
                raise UnclosedQuotationException(self.program.curr_line, self.program.curr_col, string)
            string += self.program.get_curr_char()
            self.program.advance_character()

        return Token(STRING_TOKEN_TYPE, original_pos, self.program.curr_line, string, LOW)

    def generate_char_token(self):
        # Move the character after the first single quote
        self.program.advance_character()

        original_pos = self.program.curr_col
        char = self.program.get_curr_char()

        # Move to the next single quote
        self.program.advance_character()

        if self.program.get_curr_char() != '\'':
            raise InvalidCharException(self.program.curr_line, self.program.curr_col)

        return Token(CHARACTER_TOKEN_TYPE, original_pos, self.program.curr_line, char, LOW)

    def handle_dot_character(self):
        dot_operator = self.program.get_curr_char()
        dot_operator_idx = self.program.curr_col
        if self.program.get_next_char() == ".":
            self.program.advance_character()
            dot_operator += self.program.get_curr_char()
            return Token(RANGE_INDICATION_TOKEN_TYPE, dot_operator_idx, self.program.curr_line, dot_operator, MEDIUM)
        else:
            raise InvalidTokenException(self.program.curr_line, self.program.curr_col, dot_operator)

    def handle_equal_operator(self):
        equal_idx = self.program.curr_col
        self.program.advance_character()
        return Token(EQUAL_TOKEN_TYPE, equal_idx, self.program.curr_line, "==", HIGH)

    def check_paren_pairing(self):
        # Check to make sure all the parenthesis line up accordingly.
        paren_error_row = 0
        paren_error_col = 0
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

    def check_if_else_blocks(self):
        # Confirm there is at least one `else` present, otherwise no need to
        # check if there are matching `if` blocks.
        if len(self.else_idx_list) > 0:
            # Case of there being an else with no matched if.
            if len(self.if_idx_list) < len(self.else_idx_list):
                for idx, if_idx in enumerate(reversed(self.if_idx_list)):
                    brace_count = 0
                    for token in self.token_list[if_idx:self.else_idx_list[idx]]:
                        if token.ttype == LEFT_CURL_BRACE_TOKEN_TYPE:
                            brace_count = brace_count + 1
                        elif token.ttype == RIGHT_CURL_BRACE_TOKEN_TYPE:
                            brace_count = brace_count - 1
                        else:
                            # Token does not affect determining the if/else
                            # matching algorithm.
                            pass
                    if brace_count != 0:
                        err_token = self.token_list[self.else_idx_list[idx]]
                        raise UnpairedElseError(err_token.row, err_token.col)
                # All other if/else pairs matched so the final else must be
                # the problem
                err_token = self.token_list[self.else_idx_list[-1]]
                raise UnpairedElseError(err_token.row, err_token.col)

        # If/else blocks all match, make sure there is nothing between the end
        # of an `if` block and the start of an `else` block
        filtered_token_list = list(filter(lambda token: (token.ttype != NEW_LINE_TOKEN_TYPE), self.token_list))
        for idx, token in enumerate(filtered_token_list):
            if token.value == "else" and filtered_token_list[idx - 1].ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                raise BadFormattedLogicBlock(token.row, 0)


########
# PARSER
########
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.has_next_token = True
        self.curr_token_pos = -1
        self.root_node = None
        self.variable_to_type_map = {}

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

    def peek_next_token(self):
        return self.token_list[self.curr_token_pos + 1]

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
                node = self.parse_assignment(root_node)
            elif self.curr_token.ttype == GREATER_THAN_TOKEN_TYPE:
                node = self.parse_comparator(CompareNode, root_node)
            elif self.curr_token.ttype == LESS_THAN_TOKEN_TYPE:
                node = self.parse_comparator(CompareNode, root_node)
            elif self.curr_token.ttype == EQUAL_TOKEN_TYPE:
                node = self.parse_comparator(CompareNode, root_node)
            elif self.curr_token.ttype == RANGE_INDICATION_TOKEN_TYPE:
                node = self.parse_op(RangeNode, root_node)
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
            elif self.curr_token.ttype == CHARACTER_TOKEN_TYPE:
                node = CharNode(self.curr_token, self.curr_token.value)
            elif self.curr_token.ttype == BOOLEAN_TOKEN_TYPE:
                node = BooleanNode(self.curr_token, self.curr_token.value)
            elif self.curr_token.ttype == VARIABLE_NAME_TOKEN_TYPE:
                node = VariableNode(self.curr_token, self.curr_token.value, None)
            elif self.curr_token.ttype == VARIABLE_REFERENCE_TOKEN_TYPE:
                node = VariableReferenceNode(self.curr_token, self.curr_token.value, None)
            elif self.curr_token.ttype == COMMA_TOKEN_TYPE:
                node = ArgSeparatorNode(self.curr_token)
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
            raise kme
        except InvalidTypeDeclarationException as itde:
            print_exception_message(("\n").join(program_lines), itde.col_num, itde)
            raise itde

    def parse_literal(self):
        """
        Parse a literal token.

        If we are parsing a literal token we create it but don't set the
        parent_node because it will either get set later in the parse_op on
        the creation of the op node, or it isn't linked to anything anyways.
        """
        return NumberNode(self.curr_token, self.curr_token.value, None)

    def parse_op(self, op_type, root_node):
        # This determines whether or not the root node is an operation or a
        # number and if we should replace the right side with an op
        replace_right_side_with_op = (
                type(root_node) not in [NumberNode, VariableNode, VariableReferenceNode]
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

        self.check_if_valid_operation(op_token.value, left_node, right_node)

        if replace_right_side_with_op:
            ret_node = root_node
            node.parent_node = ret_node
            ret_node.right_side = node
            return ret_node
        return node

    def parse_comparator(self, op_type, root_node):
        """
        This is just like the `parse_op` method except we don't ever want to
        take anything from either the left or right and have them mix.
        Priorities between the left and right side are not considered in this
        method.
        """
        left_node = root_node
        op_token = self.curr_token
        self.advance_token()
        right_node = None
        # Only need to loop here because the root_node being passed will have
        # already been evaluated if there is an operation there.
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
            right_node = self.process_token(right_node)
            self.advance_token()
        node = op_type(op_token, op_token.value,
                       left_side=left_node, right_side=right_node)
        self.curr_token_pos = self.curr_token_pos - 1
        self.curr_token = self.token_list[self.curr_token_pos]
        return node

    def parse_assignment(self, root_node):
        """
        This is its own method because an assignment can contain more than a
        single value and might be an expression on the right hand side.
        """
        left_node = root_node
        op_token = self.curr_token
        right_node = None
        # Peek ahead to ensure we are not getting an EOL token.
        while self.peek_next_token().ttype != EOL_TOKEN_TYPE:
            # Advance and process the token.
            self.advance_token()

            right_node = self.process_token(right_node)
        self.check_assignment_type_matching(self.variable_to_type_map.get(left_node.value), type(right_node), right_node.value)
        return AssignmentNode(op_token, op_token.value,
                              left_side=left_node, right_side=right_node)

    # NOTE(map) This method is very brittle right now.
    # TODO(map) Can these left to right side maps exist as a dict?
    def check_assignment_type_matching(self, left_side_type, right_side_type, right_side_value):
        # The `parse_assignment` could be the initial assignment of the var
        # so we need to confirm there is a type before checking if they match.
        if left_side_type:
            right_side_char = right_side_type == CharNode
            right_side_char_at = right_side_type == FunctionKeywordNode and right_side_value == "charAt"
            if left_side_type == "char" and not right_side_char and not right_side_char_at:
                raise InvalidAssignmentException(self.curr_token.row, self.curr_token.col, left_side_type, right_side_type)

    def handle_parenthesis(self):
        # This only works for numbers. For functions this will need to be
        # updated to handle those situations.
        root_node = None

        # if self.token_list[self.curr_token_pos - 1].ttype in ALL_TOKENS:
        # Advance once to get past the paren token.
        self.advance_token()

        # Currently don't care about the previous token. Keeping this in
        # so we can error out if the token isn't recognized.
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
            root_node = self.process_token(root_node)
            self.advance_token()

        return root_node

    def handle_string(self):
        return StringNode(self.curr_token, self.curr_token.value, None)

    def handle_keyword(self):
        node_value = self.curr_token.value

        # Used for logic nodes
        truth_body = None
        false_body = None
        loop_body = None

        keyword_token = self.curr_token
        # Move past keyword token
        self.advance_token()

        # Map of the functions needed to be called to parse certain tokens.
        func_map = {
            "main": (self.handle_main_keyword, StartNode, "children_nodes"),
            "const": (self.handle_const_keyword, VariableKeywordNode, "child_node"),
            "int16": (self.handle_var_declaration, VariableKeywordNode, "child_node"),
            "string": (self.handle_var_declaration, VariableKeywordNode, "child_node"),
            "char": (self.handle_var_declaration, VariableKeywordNode, "child_node"),
            "bool": (self.handle_var_declaration, VariableKeywordNode, "child_node"),
            "print": (self.handle_print_keyword, FunctionKeywordNode, "arg_nodes"),
            "printl": (self.handle_print_keyword, FunctionKeywordNode, "arg_nodes"),
            "charAt": (self.handle_char_at_keyword, FunctionKeywordNode, "arg_nodes"),
            "if": (self.handle_parenthesis, LogicKeywordNode, "child_node"),
            "loopUp": (self.handle_parenthesis, LoopUpKeywordNode, "child_node"),
            "loopDown": (self.handle_parenthesis, LoopDownKeywordNode, "child_node"),
            "loopFrom": (self.handle_parenthesis, LoopFromKeywordNode, "child_node"),
        }
        contents_function, node_class, node_args = func_map.get(node_value)
        if node_class == LogicKeywordNode:
            # Need to get the true and false body to assign to node.
            contents = contents_function()
            truth_body = self.get_truth_side()
            false_body = self.get_false_side()
        elif node_class in [LoopUpKeywordNode, LoopDownKeywordNode, LoopFromKeywordNode]:
            # Need to get contents of the loop.
            contents = contents_function()
            # TODO(map) The loop methods should have their own methods that
            # raise these exceptions.
            if not contents:
                if node_class == LoopUpKeywordNode:
                    raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, LOOP_UP_SIGNATURE)
                if node_class == LoopDownKeywordNode:
                    raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, LOOP_DOWN_SIGNATURE)
                if node_class == LoopFromKeywordNode:
                    raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, LOOP_FROM_SIGNATURE)
            loop_body = self.get_loop_body(node_value)
        else:
            contents = contents_function(keyword_token)
        kwargs = {
            "token": keyword_token,
            "value": keyword_token.value,
            node_args: contents
        }
        if truth_body:
            kwargs["true_side"] = truth_body
            kwargs["false_side"] = false_body
        if loop_body:
            kwargs["loop_body"] = loop_body

        keyword_node = node_class(**kwargs)
        return keyword_node

    def handle_main_keyword(self, keyword_token):
        """Signature is `main() { BODY };`"""
        # Confirm the left paren is right after the main keyword
        if not self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, MAIN_SIGNATURE)

        # Move past the left paren.
        self.advance_token()

        # Confirm the right paren closes the left.
        if not self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, MAIN_SIGNATURE)

        # Move pas the right paren
        self.advance_token()

        # Confirm left curl brack is present.
        if not self.curr_token.ttype == LEFT_CURL_BRACE_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, MAIN_SIGNATURE)

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
                # Add the node to the list because it is a logical unit of work
                node_list.append(root_node)
                root_node = None
            elif (isinstance(node, LogicKeywordNode) or isinstance(node, LoopKeywordNode)) and node.value in ["if", "loopUp", "loopDown", "loopFrom"]:
                # Need to add the node to the list because it is a logic unit
                # of work not ended by a semicolon.
                node_list.append(root_node)
                root_node = None
            self.advance_token()
        return node_list

    def handle_print_keyword(self, keyword_token):
        """Signature is `print(VALUE)`"""
        # Confirm the left paren is right after print keyword
        if not self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, PRINT_SIGNATURE)

        # Move past the left paren.
        self.advance_token()

        # Case where `print` was called with nothing to print.
        if self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, PRINT_SIGNATURE)

        # Parse the inner parts of the print function
        root_node = None
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
            root_node = self.process_token(root_node)
            self.advance_token()
        return [root_node]

    def handle_char_at_keyword(self, keyword_token):
        """Signature is `charAt(STRING, INDEX)`"""
        # Confirm the left paren is right after print keyword
        if not self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, CHAR_AT_SIGNATURE)

        # Move past the left paren.
        self.advance_token()

        # Case where `print` was called with nothing to print.
        if self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            raise KeywordMisuseException(keyword_token.row, keyword_token.col, keyword_token.value, CHAR_AT_SIGNATURE)

        # Parse the inner parts of the print function
        arg_list = []
        root_node = None
        while self.curr_token.ttype != RIGHT_PAREN_TOKEN_TYPE:
            node = self.process_token(root_node)
            if type(node) != ArgSeparatorNode:
                root_node = node
            if type(node) == ArgSeparatorNode:
                arg_list.append(root_node)
                root_node = None
                node = None
            self.advance_token()
        # Add the final calculated node to the list
        arg_list.append(root_node)
        return arg_list

    def handle_const_keyword(self, keyword_token):
        child_node = None
        while self.curr_token.ttype != EOL_TOKEN_TYPE:
            child_node = self.process_token(child_node)
        return child_node

    def handle_var_declaration(self, keyword_token):
        child_node = None
        while self.curr_token.ttype != EOL_TOKEN_TYPE:
            child_node = self.process_token(child_node)
            self.advance_token()

        # Put the variable and type in the map to be able to check references
        # and uses later.
        self.variable_to_type_map[child_node.left_side.value] = keyword_token.value

        # Check to see if the `char` initial assignment is the result of
        # calling the `charAt` function since that's a fair initial declaration
        assignment_is_char_at = type(child_node.right_side) == FunctionKeywordNode and child_node.right_side.value == "charAt"
        if keyword_token.value == "int16" and not child_node.right_side.value.isnumeric():
            raise InvalidTypeDeclarationException(child_node.left_side.token.row, child_node.left_side.token.col)
        elif keyword_token.value == "string" and type(child_node.right_side) != StringNode:
            raise InvalidTypeDeclarationException(child_node.left_side.token.row, child_node.left_side.token.col)
        elif keyword_token.value == "char" and type(child_node.right_side) != CharNode and not assignment_is_char_at:
            raise InvalidTypeDeclarationException(child_node.left_side.token.row, child_node.left_side.token.col)
        elif keyword_token.value == "bool" and type(child_node.right_side) != BooleanNode:
            raise InvalidTypeDeclarationException(child_node.left_side.token.row, child_node.left_side.token.col)
        else:
            return child_node

    def get_truth_side(self):
        truth_body = None
        truth_node_list = []
        # Move past closing paren on conditional check
        self.advance_token()

        # Move past left curl bracket
        self.advance_token()

        while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
            ret_node = self.process_token(truth_body)
            if type(ret_node) != NoOpNode:
                truth_body = ret_node
            self.advance_token()
            if self.curr_token.ttype == EOL_TOKEN_TYPE or type(ret_node) == LogicKeywordNode:
                truth_node_list.append(truth_body)
                truth_body = None

        # We don't want to move past the curl brace that closes the if
        # statement because the `handle_main` will always be stepping over it
        # as part of its processing.

        return truth_node_list

    def get_false_side(self):
        false_body = None
        # Flag if there is an else keyword and parse it.
        is_else_keyword_present = self.peek_next_token().value == "else"
        false_node_list = []
        if is_else_keyword_present:
            # Move beyond the closing right curl brace of the `if` statment
            self.advance_token()

            # Move past the else keyword.
            self.advance_token()

            # Move past the curl bracket that starts the else body.
            self.advance_token()

            while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                ret_node = self.process_token(false_body)
                if type(ret_node) != NoOpNode:
                    false_body = ret_node
                self.advance_token()
                if self.curr_token.ttype == EOL_TOKEN_TYPE or type(ret_node) == LogicKeywordNode:
                    false_node_list.append(ret_node)
                    false_body = None
        return false_node_list

    def get_loop_body(self, node_value):
        # Move past right paren
        self.advance_token()

        loop_contents = []
        loop_body = None

        while self.curr_token.ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
            ret_node = self.process_token(loop_body)
            if type(ret_node) != NoOpNode:
                loop_body = ret_node
            self.advance_token()
            if self.curr_token.ttype == EOL_TOKEN_TYPE or type(ret_node) in [LogicKeywordNode, LoopUpKeywordNode, LoopDownKeywordNode]:
                loop_contents.append(loop_body)
                loop_body = None

        if node_value not in ["loopUp", "loopDown", "loopFrom"]:
            assert False, f"Loop of type {node_value} is not recognized."
        else:
            return loop_contents

    def check_if_valid_operation(self, op_type, left_node, right_node):
        # Checking for add operation being of the same type.
        if op_type == "+":
            if type(left_node) == VariableReferenceNode and self.variable_to_type_map[left_node.value] == "string" and type(right_node) != CharNode:
                raise InvalidConcatenationException(left_node.token.row, left_node.token.col, self.variable_to_type_map[left_node.value], type(right_node))
        # TODO(map) Implement the checks for all the other op types.
        else:
            pass



##########
# Compiler
##########
class Compiler:

    def __init__(self, ast):
        self.ast = ast
        self.output_path = os.getcwd() + "/out.asm"
        self.string_count = 0
        self.char_count = 0
        self.bool_count = 0
        self.num_count = 0
        self.var_count = 0
        self.raw_string_count = 0
        self.raw_char_count = 0
        self.conditional_count = 0
        self.loop_count = 0
        self.raw_strings = {}
        self.raw_chars = {}
        self.variables = {}
        self.conditionals = {}
        self.loops = {}
        self.initialize_vars_asm = []

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
            # Write any raw chars that will be used that aren't assigned to a
            # variable in the code.
            for key in self.raw_chars:
                for line in self.raw_chars[key]:
                    compiled_program.write(line)
            # Write the variables first, them move to assembly.
            for key in self.variables:
                # Write the assembly for the string.
                for line in self.variables[key]["asm"]:
                    compiled_program.write(line)
            self.create_start_point(compiled_program)
            for line in self.initialize_vars_asm:
                compiled_program.write(line)
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
                if node.can_traverse_to_parent():
                    return self.process_op_node(node) + self.traverse_tree(node.parent_node)
                else:
                    return self.process_op_node(node)
        elif isinstance(node, NumberNode):
            node.visited = True
            if type(node.parent_node) == AssignmentNode:
                return [] + self.traverse_tree(node.parent_node)
            elif node.can_traverse_to_parent():
                return self.get_push_number_onto_stack_asm(node.value) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_number_onto_stack_asm(node.value)
        elif isinstance(node, FunctionKeywordNode):
            asm = []
            if node.value == "print":
                if type(node.arg_nodes[0]) == StringNode:
                    keyword_call_asm = self.get_print_string_keyword_asm()
                elif type(node.arg_nodes[0]) == NumberNode:
                    keyword_call_asm = self.get_print_num_keyword_asm()
                elif type(node.arg_nodes[0]) == CharNode:
                    keyword_call_asm = self.get_print_char_keyword_asm()
                elif self.variables[node.arg_nodes[0].value]:
                    if self.variables[node.arg_nodes[0].value]["var_type"] == "string":
                        keyword_call_asm = self.get_print_string_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "char":
                        keyword_call_asm = self.get_print_char_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "num":
                        keyword_call_asm = self.get_print_num_keyword_asm()
            elif node.value == "printl":
                if type(node.arg_nodes[0]) == StringNode:
                    keyword_call_asm = self.get_printl_string_keyword_asm()
                elif type(node.arg_nodes[0]) == NumberNode:
                    keyword_call_asm = self.get_printl_num_keyword_asm()
                elif type(node.arg_nodes[0]) == CharNode:
                    keyword_call_asm = self.get_printl_char_keyword_asm()
                elif self.variables[node.arg_nodes[0].value]:
                    if self.variables[node.arg_nodes[0].value]["var_type"] == "string":
                        keyword_call_asm = self.get_printl_string_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "char":
                        keyword_call_asm = self.get_printl_char_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "num":
                        keyword_call_asm = self.get_printl_num_keyword_asm()
            elif node.value == "charAt":
                keyword_call_asm = self.get_char_at_keyword_asm()
            else:
                # We don't know how to parse this keyword.
                assert False, f"Unable to parse Function Keyword Node {node}"
            for arg_node in node.arg_nodes:
                if not arg_node.visited:
                    asm.extend(self.traverse_tree(arg_node))
            if node.can_traverse_to_parent():
                node.visited = True
                return asm + keyword_call_asm + self.traverse_tree(node.parent_node)
            else:
                node.visted = True
                return asm + keyword_call_asm
        elif isinstance(node, VariableKeywordNode):
            if node.child_node and not node.child_node.visited:
                return self.traverse_tree(node.child_node)
            elif node.can_traverse_to_parent():
                node.visited = True
                return self.traverse_tree(node.parent_node)
            else:
                node.visted = True
                return []
        elif isinstance(node, StringNode):
            node.visited = True
            self.raw_string_count += 1
            key = f"raw_string_{self.raw_string_count}"
            self.raw_strings[key] = self.get_raw_string_asm(node.value, len(node.value), self.raw_string_count)
            if node.can_traverse_to_parent():
                return self.get_push_string_asm(self.raw_string_count, len(node.value)) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_string_asm(self.raw_string_count, len(node.value))
        elif isinstance(node, CharNode):
            node.visited = True
            self.raw_char_count += 1
            key = f"raw_char_{self.raw_char_count}"
            self.raw_chars[key] = self.get_raw_char_asm(node.value, self.raw_char_count)
            if node.can_traverse_to_parent():
                return self.get_push_char_asm(self.raw_char_count) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_char_asm(self.raw_char_count)
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

            if type(value_node) == StringNode:
                self.string_count += 1
                var_name = f"string_{self.string_count}"
                var_type = "string"
                type_count = self.string_count
            elif type(value_node) == CharNode:
                self.char_count += 1
                var_name = f"char_{self.char_count}"
                var_type = "char"
                type_count = self.char_count
            elif type(value_node) == NumberNode:
                self.num_count += 1
                var_name = f"number_{self.num_count}"
                var_type = "num"
                type_count = self.num_count
            elif type(value_node) == BooleanNode:
                self.bool_count += 1
                var_name = f"bool_{self.bool_count}"
                var_type = "bool"
                type_count = self.bool_count
            elif value_node.value == "charAt" and type(value_node) == FunctionKeywordNode:
                self.char_count += 1
                var_name = f"char_{self.char_count}"
                type_count = self.char_count
                var_type = "char"
                self.initialize_vars_asm.extend(self.traverse_tree(value_node))
                self.initialize_vars_asm.extend(self.get_assign_char_at_value_to_var_asm(var_name))
            else:
                assert False, f"Not sure how to handle Variable of type {type(value_node)} with value {value_node.value}"
            # Check if the variable has the const keyword associated with it.
            if node.parent_node.parent_node.parent_node.value == "const":
                asm = self.get_const_creation_asm(self.var_count, type_count, value_node.value, type(value_node))
            else:
                asm = self.get_var_creation_asm(self.var_count, type_count, value_node.value, type(value_node))
            self.variables[node.value] = {
                "section":  section_text,
                "var_name": var_name,
                "var_type": var_type,
                "var_len": len(value_node.value),
                "asm": asm
            }
            return self.traverse_tree(node.parent_node)
        elif isinstance(node, VariableReferenceNode):
            node.visited = True
            # If the ref node is the left node of an assignment we don't need
            # to push this onto the stack because the assignment assembly will
            # push the variable onto the stack during assignment.
            if type(node.parent_node) == AssignmentNode and node.parent_node.left_side.value == node.value:
                if node.can_traverse_to_parent():
                    return [] + self.traverse_tree(node.parent_node)
                else:
                    return []
            elif type(node.parent_node) == AssignmentNode and type(node) in [NumberNode, VariableReferenceNode]:
                # Case of right side of assignment is just a var
                if node.can_traverse_to_parent():
                    var_ref = self.variables[node.value]["var_name"]
                    return [
                        f"    push qword [{var_ref}]\n",
                        "    pop rax\n"
                    ] + self.traverse_tree(node.parent_node)
                else:
                    return []
            # Case of referencing a node and needing it on the stack (ie print)
            var_ref = self.variables[node.value]["var_name"]
            var_len = self.variables[node.value]["var_len"]
            if node.can_traverse_to_parent():
                return self.get_push_var_onto_stack_asm(var_ref, var_len) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_var_onto_stack_asm(var_ref, var_len)
        elif isinstance(node, LogicKeywordNode):
            node.visited = True
            if not node.child_node.visited:
                return self.traverse_tree(node.child_node)
            conditional_mark_count = self.conditionals[node.child_node]
            if node.child_node.value == ">":
                return self.traverse_greater_than_body(conditional_mark_count, node) + self.get_end_of_conditional_asm(conditional_mark_count)
            elif node.child_node.value == "<":
                return self.traverse_less_than_body(conditional_mark_count, node) + self.get_end_of_conditional_asm(conditional_mark_count)
            elif node.child_node.value == "==":
                return self.traverse_equal_body(conditional_mark_count, node) + self.get_end_of_conditional_asm(conditional_mark_count)
            else:
                assert False, f"Conditional {node.child_nod.value} not understood."
        elif isinstance(node, LoopKeywordNode):
            if type(node) == LoopUpKeywordNode:
                node.visited = True
                if not node.child_node.visited:
                    return self.get_push_loop_start_val_asm(0) + self.traverse_tree(node.child_node)
                if not node.loop_body[0].visited:
                    self.loop_count += 1
                    self.loops[node] = self.loop_count
                    return  self.get_loop_up_asm_start(self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_asm_end(self.loops[node])
                return []
            elif type(node) == LoopDownKeywordNode:
                node.visited = True
                if not node.child_node.visited:
                    return self.get_push_loop_end_val_asm(0) + self.traverse_tree(node.child_node)
                if not node.loop_body[0].visited:
                    self.loop_count += 1
                    self.loops[node] = self.loop_count
                    return self.get_loop_down_asm_start(self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(self.loops[node])
                return []
            elif type(node) == LoopFromKeywordNode:
                node.visited = True
                if node.child_node.left_side.value < node.child_node.right_side.value:
                    if not node.child_node.visited:
                        return ["    ;; Push loop start and end on stack\n"] + self.traverse_tree(node.child_node)
                    if not node.loop_body[0].visited:
                        self.loop_count += 1
                        self.loops[node] = self.loop_count
                        return self.get_loop_up_asm_start(self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_from_ascending_asm(self.loops[node])
                    return []
                else:
                    if not node.child_node.visited:
                        return ["    ;; Push loop start and end on stack\n"] + self.traverse_tree(node.child_node)
                    if not node.loop_body[0].visited:
                        self.loop_count += 1
                        self.loops[node] = self.loop_count
                        return self.get_loop_down_asm_start(self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_from_descending_asm(self.loops[node])
                    return []
        elif type(node) == BooleanNode:
            node.visited = True
            if type(node.parent_node) == AssignmentNode:
                return [] + self.traverse_tree(node.parent_node)
            elif node.can_traverse_to_parent():
                return self.get_push_boolean_onto_stack(node.value) + self.traverse_tree(node.parent_node)
            return self.get_push_boolean_onto_stack(node.value)
        elif type(node) == CharNode:
            node.visisted = True
            # We just need to return to the parent node because we would never
            # push the byte itself onto the stack here.
            if node.can_traverse_to_parent():
                return [] + self.traverse_tree(node.parent_node)
            return []
        else:
            assert False, (f"This node type {type(node)} is not yet implemented.")

    def traverse_greater_than_body(self, conditional_key, node):
        logic_asm = []
        if node.true_side:
            logic_asm += self.get_true_side_asm(conditional_key) + self.traverse_logic_node_children(node.true_side) + self.get_jump_false_condition_body(conditional_key)
        if node.false_side:
            logic_asm += self.get_false_side_asm(conditional_key) + self.traverse_logic_node_children(node.false_side)
        else:
            logic_asm += self.get_false_side_asm(conditional_key)
        return logic_asm

    def traverse_less_than_body(self, conditional_key, node):
        logic_asm = []
        if node.true_side:
            logic_asm += self.get_false_side_asm(conditional_key) + self.traverse_logic_node_children(node.true_side) + self.get_jump_false_condition_body(conditional_key)
        if node.false_side:
            logic_asm += self.get_true_side_asm(conditional_key) + self.traverse_logic_node_children(node.false_side)
        else:
            logic_asm += self.get_true_side_asm(conditional_key)
        return logic_asm

    def traverse_equal_body(self, conditional_key, node):
        logic_asm = []
        if node.true_side:
            logic_asm += self.get_equal_side_asm(conditional_key) + self.traverse_logic_node_children(node.true_side) + self.get_jump_false_condition_body(conditional_key)
        if node.false_side:
            logic_asm += self.get_not_equal_side_asm(conditional_key) + self.traverse_logic_node_children(node.false_side)
        else:
            logic_asm += self.get_not_equal_side_asm(conditional_key)
        return logic_asm

    def traverse_logic_node_children(self, children):
        child_asm = []
        for child in children:
            if not child.visited:
                child.visited = True
                child_asm += self.traverse_tree(child)
        return child_asm

    def process_op_node(self, node):
        if node.value == "+":
            # Check if the left side of the add if a variable and its type. If
            # it's a string we don't want to do the basic add assembly.
            if type(node.left_side) == VariableReferenceNode and self.variables[node.left_side.value]["var_type"] == "string":
                return self.get_string_concat_asm(node.left_side.value, self.variables[node.left_side.value]["var_len"])
            else:
                return self.get_add_asm()
        elif node.value == "-":
            return self.get_sub_asm()
        elif node.value == "*":
            return self.get_mul_asm()
        elif node.value == "/":
            return self.get_div_asm()
        elif node.value == ">":
            self.conditional_count += 1
            self.conditionals[node] = self.conditional_count
            return self.get_conditional_greater_than_asm(self.conditional_count)
        elif node.value == "<":
            self.conditional_count += 1
            self.conditionals[node] = self.conditional_count
            return self.get_conditional_less_than_asm(self.conditional_count)
        elif node.value == "==":
            self.conditional_count += 1
            self.conditionals[node] = self.conditional_count
            if type(node.left_side) == CharNode or type(node.right_side) == CharNode:
                compare_types = "char"
            else:
                compare_types = "int16"
            return self.get_conditional_equal_asm(self.conditional_count, compare_types)
        elif node.value == "=":
            print(f"Should be assigning for node {node}")
            # This is an assignment of a new value to the variable.
            if type(node.parent_node) != VariableKeywordNode:
                # If the right side of the assignment is an expression then we
                # don't need to pop any values to clean up because the assembly
                # will pop the data to do the expression.
                if type(node.right_side) == PlusMinusNode:
                    if self.variables[node.left_side.value]["var_type"] == "string":
                        # Do not return the standard assignment of string as we
                        # are doing a concat on the string.
                        return []
                    else:
                        # Otherwise get the standard assignment asm for plus or
                        # minus token.
                        return self.get_assign_new_value_to_var_from_expression(self.variables[node.left_side.value]["var_name"])
                elif type(node.right_side) == MultiplyDivideNode:
                    return self.get_assign_new_value_to_var_from_expression(self.variables[node.left_side.value]["var_name"])
                elif node.right_side.value == "charAt":
                    return self.get_assign_char_at_value_to_var_asm(self.variables[node.left_side.value]["var_name"])
                elif type(node.right_side) == CharNode:
                    return self.get_assign_char_value_to_var_asm(self.variables[node.left_side.value]["var_name"])
                elif type(node.right_side) == StringNode:
                    # TODO(map) Handle updating string.
                    # This seems like it'll be a char by char thing.
                    assert False, "Not implemented."
                elif type(node.right_side) == NumberNode:
                    return self.get_get_assign_int_value_to_var_asm(self.variables[node.left_side.value]["var_name"], node.right_side.value)
                elif type(node.right_side) == VariableReferenceNode:
                    return self.get_assign_new_value_from_var_to_var_asm(self.variables[node.left_side.value]["var_name"])
                else:
                    return self.get_assign_new_value_to_var_asm(self.variables[node.left_side.value]["var_name"], node.right_side.value)
            # Don't do anything if the parent is an AssignmentNode because the
            # parent_node will handle that assembly.
            print(f"Node not doing anything {node}")
            return []
        elif node.value == "..":
            # Don't need to get assembly here because the loop will handle it.
            return []
        else:
            assert False, f"Unrecognized root node value {node.value}"

    def create_keyword_functions(self):
        self.create_print_string_function()
        self.create_print_num_function()
        self.create_print_char_function()
        self.create_printl_string_function()
        self.create_printl_num_function()
        self.create_printl_char_function()
        self.create_char_at_function()
        self.create_string_length()

    def create_print_string_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    print_string:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get variable value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Get variable length\n")
            compiled_program.write("        pop rdx\n")
            compiled_program.write("        mov rsi, rax\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")

    def create_print_num_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    print_num:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get variable value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        add rax, 48\n")
            compiled_program.write("        push rax\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")
    
    def create_print_char_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    print_char:\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        mov rdx, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("         ;; Push return address back.\n")
            compiled_program.write("         push rbx\n")
            compiled_program.write("         ret\n")
 
    def create_printl_string_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    printl_string:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get variable value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Get variable length\n")
            compiled_program.write("        pop rdx\n")
            compiled_program.write("        mov rsi, rax\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Add linefeed.\n")
            compiled_program.write("        push 10\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Add return carriage.\n")
            compiled_program.write("        push 13\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")

    def create_printl_num_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    printl_num:\n")
            compiled_program.write("        ;; Print function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get variable value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        add rax, 48\n")
            compiled_program.write("        push rax\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Add linefeed.\n")
            compiled_program.write("        push 10\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Add return carriage.\n")
            compiled_program.write("        push 13\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Push return address back.\n")
            compiled_program.write("        push rbx\n")
            compiled_program.write("        ret\n")
    
    def create_printl_char_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    printl_char:\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        mov rdx, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Add linefeed.\n")
            compiled_program.write("        push 10\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Add return carriage.\n")
            compiled_program.write("        push 13\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Remove value at top of stack.\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("         ;; Push return address back.\n")
            compiled_program.write("         push rbx\n")
            compiled_program.write("         ret\n")

    def create_char_at_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    char_at:\n")
            compiled_program.write("        ;; charAt function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rcx\n")
            compiled_program.write("        ;; Get char index\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get string value\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Pop string length\n")
            compiled_program.write("        pop rdx\n")
            compiled_program.write("        ;; Get byte of string at index\n")
            compiled_program.write("        mov dl, [rax + rbx]\n")
            compiled_program.write("        ;; Push byte back onto stack\n")
            compiled_program.write("        push dx\n")
            compiled_program.write("        ;; Push return address onto stack\n")
            compiled_program.write("        push rcx\n")
            compiled_program.write("        ret\n")

    def create_string_length(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    string_length:\n")
            compiled_program.write("        ;; strLen function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rcx\n")
            compiled_program.write("        ;; Get the first string reference\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get the second string reference\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        loop_str_len:\n")
            compiled_program.write("            cmp byte[rax], 0\n")
            compiled_program.write("            jne loop_again\n")
            compiled_program.write("            je end_str_len\n")
            compiled_program.write("        loop_again:\n")
            compiled_program.write("            inc rax\n")
            compiled_program.write("            jmp loop_str_len\n")
            compiled_program.write("        end_str_len:\n")
            compiled_program.write("            ;; Calculate actual difference in length\n")
            compiled_program.write("            sub rax, rbx\n")
            compiled_program.write("            push rax\n")
            compiled_program.write("            ;; Push return address onto stack\n")
            compiled_program.write("        ;; Push return address onto stack\n")
            compiled_program.write("        push rcx\n")
            compiled_program.write("        ret\n")

    def create_global_start(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    global _start\n")

    def get_push_number_onto_stack_asm(self, num):
        return [
            "    ;; Push number onto stack\n",
            f"    push {num}\n"
            ]

    def get_push_var_onto_stack_asm(self, val, val_len):
        if "string" in val:
            return [
                "    ;; Calculate string length and push onto stack with string\n",
                f"    push {val}\n",
                f"    push {val}\n",
                "    call string_length\n",
                f"    push {val}\n"
            ]
        elif "char" in val:
            return [
                "    ;; Push char var onto stack\n",
                f"    mov bl, [{val}]\n",
                f"    push bx\n"
            ]
        return [
            "    ;; Push var val onto stack\n",
            f"    push qword [{val}]\n",
        ]

    def get_push_boolean_onto_stack(self, node_value):
        if node_value == "true":
            return [
                "    ;; Push true onto stack\n",
                "    push 1\n"
            ]
        else:
            return [
                "    ;; Push false onto stack\n",
                "    push 0\n"
            ]

    def get_add_asm(self):
        return ["    ;; Add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    add rax, rbx\n",
                "    push rax\n"]

    def get_string_concat_asm(self, val, string_len):
        # Update the length of the string to the new value.
        self.variables[val]["var_len"] += 1
        return [
            "    ;; Concat string\n",
            "    pop ax\n",
            "    pop rbx\n",
            "    ;; Remove string length from stack\n",
            "    pop rcx\n",
            "    ;; Append char to string\n",
            f"    mov byte [rbx+rcx], al\n",
        ]

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

    def get_print_string_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call print_string\n"
        ]

    def get_printl_string_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call printl_string\n"
        ]

    def get_print_num_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call print_num\n"
        ]

    def get_printl_num_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call printl_num\n"
        ]

    def get_print_char_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call print_char\n",
            "    ;; Pop the byte off the stack to clean up\n",
            "    pop bx\n",
        ]

    def get_printl_char_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call printl_char\n",
            "    ;; Pop the byte off the stack to clean up\n",
            "    pop bx\n",
        ]

    def get_char_at_keyword_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call char_at\n"
        ]

    def get_push_loop_start_val_asm(self, loop_start):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    push {loop_start}\n"
        ]

    def get_push_loop_end_val_asm(self, loop_end):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    push {loop_end}\n"
        ]


    def get_loop_up_asm_start(self, loop_count):
        return [
            "    ;; Loop up\n",
            f"    loop_{loop_count}:\n",
        ]

    def get_loop_down_asm_start(self, loop_count):
        return [
            "    ;; Loop down\n",
            f"    loop_{loop_count}:\n",
        ]

    def get_loop_up_asm_end(self, loop_count):
        return [
            "    ;; Compare if counter is below loop end\n",
            "    pop rbx\n",
            "    pop rcx\n",
            "    inc rcx\n",
            "    cmp rcx, rbx\n",
            "    push rcx\n",
            "    push rbx\n",
            f"    jl loop_{loop_count}\n",
            "    ;; Clean up loop vars\n",
            "    pop rax\n",
            "    pop rax\n"
        ]

    def get_loop_down_asm_end(self, loop_count):
        return [
            "    ;; Compare if counter is above loop end\n",
            "    pop rcx\n",
            "    pop rbx\n",
            "    dec rcx\n",
            "    cmp rcx, rbx\n",
            "    push rbx\n",
            "    push rcx\n",
            f"    jg loop_{loop_count}\n",
            "    ;; Clean up loop vars\n",
            "    pop rax\n",
            "    pop rax\n"
        ]

    def get_loop_from_ascending_asm(self, loop_count):
        return [
            "    ;; Compare if counter is below loop end\n",
            "    pop rbx\n",
            "    pop rcx\n",
            "    inc rcx\n",
            "    cmp rcx, rbx\n",
            "    push rcx\n",
            "    push rbx\n",
            f"    jl loop_{loop_count}\n",
            "    ;; Clean up loop vars\n",
            "    pop rax\n",
            "    pop rax\n"
        ]

    def get_loop_from_descending_asm(self, loop_count):
        return [
            "    ;; Compare if counter is above loop end\n",
            "    pop rbx\n",
            "    pop rcx\n",
            "    dec rcx\n",
            "    cmp rcx, rbx\n",
            "    push rcx\n",
            "    push rbx\n",
            f"    jg loop_{loop_count}\n",
            "    ;; Clean up loop vars\n",
            "    pop rax\n",
            "    pop rax\n"
        ]

    def get_true_side_asm(self, conditional_count):
        return [
            f"    greater_{conditional_count}:\n",
        ]

    def get_false_side_asm(self, conditional_count):
        return [
            f"    less_{conditional_count}:\n",
        ]

    def get_equal_side_asm(self, conditional_count):
        return [
            f"    equal_{conditional_count}:\n",
        ]

    def get_not_equal_side_asm(self, conditional_count):
        return [
            f"    not_equal_{conditional_count}:\n",
        ]

    def get_jump_false_condition_body(self, conditional_count):
        return [
            f"    jmp end_{conditional_count}\n"
        ]

    def get_end_of_conditional_asm(self, conditional_count):
        return [
            "    ;; End if/else block\n",
            f"    end_{conditional_count}:\n"
        ]

    def get_conditional_greater_than_asm(self, conditional_count):
        return [
            "    ;; Pop values for comparing greater than\n",
            "    pop rax\n",
            "    pop rbx\n",
            "    cmp rbx, rax\n",
            f"    jg greater_{conditional_count}\n",
            f"    jle less_{conditional_count}\n"
        ]

    def get_conditional_less_than_asm(self, conditional_count):
        return [
            "    ;; Pop values for comparing less than\n",
            "    pop rax\n",
            "    pop rbx\n",
            "    cmp rbx, rax\n",
            f"    jl less_{conditional_count}\n",
            f"    jge greater_{conditional_count}\n"
        ]

    def get_conditional_equal_asm(self, conditional_count, compare_types):
        if compare_types == "char":
            return [
                "    ;; Pop values for comparing equal on char\n",
                "    pop ax\n",
                "    pop bx\n",
                "    cmp bx, ax\n",
                f"    je equal_{conditional_count}\n",
                f"    jne not_equal_{conditional_count}\n"
            ]
        else:
            return [
                "    ;; Pop values for comparing equal on other\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    cmp rbx, rax\n",
                f"    je equal_{conditional_count}\n",
                f"    jne not_equal_{conditional_count}\n"
            ]

    def get_raw_string_asm(self, string, string_length, string_count):
        string = string.replace("\\n", "',10,13,'")
        return [
            f"section .raw_string_{string_count}\n",
            f"    raw_string_{string_count} db '{string}', 0\n",
            f"    raw_len_{string_count} equ $ - raw_string_{string_count}\n"
        ]

    def get_raw_char_asm(self, char, char_count):
        return [
            f"section .raw_char_{char_count}\n",
            f"    raw_char_{char_count} db '{char}', 0\n",
        ]

    def get_string_asm(self, string, string_length, string_count):
        string = string.replace("\\n", "',10,13,'")
        return [
            f"section .string_{string_count}\n",
            f"    string_{string_count} db '{string}', 0\n",
            f"    len_{string_count} equ $ - string_{string_count}\n"
        ]

    def get_push_string_asm(self, string_count, string_length):
        return [
            "    ;; Push a raw string and length onto stack\n",
            f"    push {string_length}\n",
            f"    push raw_string_{string_count}\n",
        ]

    def get_push_char_asm(self, char_count):
        return [
            "    ;; Push a raw char onto the stack\n",
            f"    mov bl, [raw_char_{char_count}]\n",
            f"    push bx\n",
        ]

    def get_const_creation_asm(self, var_count, type_count, value, var_type):
        if var_type == StringNode:
            var_decl = [
                f"    string_{type_count} db '{value}', 0\n",
            ]
        elif var_type == CharNode:
            var_decl = [
                f"    char_{type_count} db '{value}', 0\n",
            ]
        elif var_type == BooleanNode:
            var_decl = [
                f"    bool_{type_count} dq 0\n",
                ] if value == "false" else [
                    f"    bool_{type_count} dq 1\n",
                ]
        elif value == "charAt":
            # Case where we are initializing a variable to the return of a
            # method. We should initialized to 0, then update in the assembly.
            var_decl = [
                f"    char_{type_count} db 0\n",
            ]
        else:
            var_decl = [f"    number_{type_count} dq {value}\n"]
        return [
            f"section .var_{var_count}\n",
        ] + var_decl

    def get_var_creation_asm(self, var_count, type_count, value, var_type):
        if var_type == CharNode:
            var_decl = [
                f"    char_{type_count} db '{value}', 0\n",
            ]
        elif var_type == NumberNode:
            var_decl = [
                f"    number_{type_count} dq {value}\n",
            ]
        elif var_type == BooleanNode:
            var_decl = [
                f"    bool_{type_count} dq 0\n",
            ] if value == "false" else [
                f"    bool_{type_count} dq 1\n",
            ]
        elif value == "charAt":
            # Case where we are initializing a variable to the return of a
            # method. We should initialized to -1, then update in the assembly.
            var_decl = [
                f"    char_{type_count} db -1\n",
            ]
        # elif var_type == StringNode:
        #     var_decl = [
        #         f"    string_{type_count} db '{value}', 0\n",
        #     ]
        else:
            assert False, f"Cannot declare var of type {var_type} that is mutable."
        return [
            f"section .var_{var_count} write\n",
        ] + var_decl


    def get_assign_char_value_to_var_asm(self, var_name):
        return [
            "    ;; Assign new value to char var\n",
            f"    mov rdi, {var_name}\n",
            "    mov byte [rdi], bl\n",
            "    pop bx\n"
        ]

    def get_get_assign_int_value_to_var_asm(self, var_name, new_value):
        return [
            "    ;; Assign new int to int var\n",
            f"    mov word [{var_name}], {new_value}\n",
        ]

    def get_assign_new_string_to_var_asm(self, var_name, new_value):
        return [
            "    ;; Assign new string to string var\n",
            f"    mov word [{var_name}], '{new_value}'\n",
        ]

    def get_assign_new_value_to_var_asm(self, var_name, new_value):
        if new_value == "true":
            new_value = 1
        elif new_value == "false":
            new_value = 0
        return [
            "    ;; Assign new bool to bool var\n",
            f"    mov word [{var_name}], {new_value}\n",
        ]

    def get_assign_new_value_from_var_to_var_asm(self, var_name):
        return [
            "    ;; Assign var value to new var\n",
            f"    mov qword [{var_name}], rax\n",
        ]

    def get_assign_new_value_to_var_from_expression(self, var_name):
        return [
            "    ;; Assign expression value to new var\n",
            "    pop rax\n",
            f"    mov qword [{var_name}], rax\n",
        ]

    def get_assign_char_at_value_to_var_asm(self, var_name):
        return [
            "    ;; Pop return value of char at\n",
            "    pop ax\n",
            "    ;; Update var with value\n",
            f"    mov rdi, {var_name}\n",
            "    mov byte [rdi], al\n",
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
program_lines = []
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--program", help="The program that should be parse.")
    arg_parser.add_argument("--verbose", action="store_true",
                            help="Adds verbosity output to the steps.")
    arg_parser.add_argument("--no-raise", action="store_false",
                            help="Avoids assertions in the __eq__ methods.")
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
    raise_assertion_flag = args.no_raise
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
