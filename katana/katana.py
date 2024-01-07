import argparse
import copy
import os
import sys

# TODO(map) Move all the classes and enums outs so imports are nice
#########
# GLOBALS
#########
verbose_flag = False
raise_assertion_flag = False


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
COLON_TOKEN_TYPE = "COLON"
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
LOOP_INDEX_KEYWORD_TOKEN_TYPE = "LOOP_INDEX_KEYWORD"
FUNCTION_KEYWORD_TOKEN_TYPE = "FUNCTION_KEYWORD"
FUNCTION_NAME_TOKEN_TYPE = "FUNCTION_NAME"
FUNCTION_SEPARATOR_TOKEN_TYPE = "FUNCTION_SEPARATOR"
FUNCTION_RETURN_TOKEN_TYPE = "FUNCTION_RETURN"
FUNCTION_ARG_TOKEN_TYPE = "FUNCTION_ARG"
FUNCTION_ARG_SEPARATOR_TYPE_TOKEN_TYPE = "FUNCTION_ARG_SEPARATOR"
FUNCTION_ARG_TYPE_TOKEN_TYPE = "FUNCTION_ARG_TYPE"
FUNCTION_RETURN_KEYWORD_TOKEN_TYPE = "FUNCTION_RETURN_KEYWORD"
FUNCTION_ARG_REFERENCE_TOKEN_TYPE = "FUNCTION_ARG_REFERENCE"
FUNCTION_REFERENCE_TOKEN_TYPE = "FUNCTION_REFERENCE"
MACRO_KEYWORD_TOKEN_TYPE = "MACRO_KEYWORD"
MACRO_NAME_TOKEN_TYPE = "MACRO_NAME"
MACRO_REFERENCE_TOKEN_TYPE = "MACRO_REFERENCE"
RANGE_INDICATION_TOKEN_TYPE = "RANGE"
RIGHT_CURL_BRACE_TOKEN_TYPE = "RIGHT_CURL_BRACE"
RIGHT_PAREN_TOKEN_TYPE = "RIGHT_PAREN"
STRING_TOKEN_TYPE = "STRING"
SPACE_TOKEN_TYPE = "SPACE"
EOL_TOKEN_TYPE = "EOL"
EOF_TOKEN_TYPE = "EOF"
VARIABLE_NAME_TOKEN_TYPE = "VARIABLE_NAME"
VARIABLE_REFERENCE_TOKEN_TYPE = "VARIABLE_REFERENCE"

###########
# Var Types
###########
INT_8 = "int8"
INT_16 = "int16"
INT_32 = "int32"
INT_64 = "int64"
BOOL = "bool"
CHAR = "char"
STRING = "string"
CONST = "const"


###################
# Function Keywords
###################
PRINT = "print"
PRINTL = "printl"
MAIN = "main"
CHAR_AT = "charAt"
UPDATE_CHAR = "updateChar"
COPY_STR = "copyStr"
FN = "fn"
MACRO = "MACRO"


################
# Logic Keywords
################
IF = "if"
ELSE = "else"
LOOP_UP = "loopUp"
I_LOOP_UP = "iLoopUp"
LOOP_DOWN = "loopDown"
I_LOOP_DOWN = "iLoopDown"
LOOP_FROM = "loopFrom"
I_LOOP_FROM = "iLoopFrom"


##############
# Const tuples
##############
TOP_LEVEL_TOKENS = (
    MAIN,
    FN,
    MACRO
)
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
IGNORE_TOKENS = (SPACE_TOKEN_TYPE, COLON_TOKEN_TYPE)
IGNORE_OPS = (
    SPACE_TOKEN_TYPE,
    FUNCTION_ARG_SEPARATOR_TYPE_TOKEN_TYPE,
    FUNCTION_ARG_TYPE_TOKEN_TYPE,
    COMMENT_TOKEN_TYPE,
    NEW_LINE_TOKEN_TYPE,
)
FUNCTION_KEYWORDS = (PRINT, PRINTL, MAIN, CHAR_AT, UPDATE_CHAR, COPY_STR)
LOGIC_KEYWORDS = (IF, ELSE, I_LOOP_UP, I_LOOP_DOWN, I_LOOP_FROM, LOOP_UP, LOOP_DOWN, LOOP_FROM)
VARIABLE_KEYWORDS = (CONST, INT_8, INT_16, INT_32, INT_64, STRING, BOOL, CHAR)
INT_KEYWORDS = (INT_8, INT_16, INT_32, INT_64)

##################
# Assignment Types
##################
NUMERIC = "numeric"
FUNCTION = "function"


###################
# Method Signatures
###################
CHAR_AT_SIGNATURE = "charAt(STRING, INDEX): extracts the character at INDEX from the STRING"
COPY_STR_SIGNATURE = "copyStr(STRING_1, STRING_2): copies the contents of STRING_1 into STRING_2"
UPDATE_CHAR_SIGNATURE = "udpateChar(STRING, INDEX, NEW_CHAR);: update the character of the STRING at INDEX to the NEW_CHAR"
MAIN_SIGNATURE = "main() { BODY; };: Executes the BODY of code within the main method."
PRINT_SIGNATURE = "print(VALUE);: prints the VALUE to the screen"
LOOP_UP_SIGNATURE = "loopUp(VALUE) { BODY; }: Loops from 0 to VALUE executing BODY each time"
LOOP_DOWN_SIGNATURE = "loopDown(VALUE) { BODY; }: Loops from VALUE to 0 executing BODY each time"
LOOP_FROM_SIGNATURE = "loopFrom(START..END) { BODY; }: Loops from START to END executing BODY each time"
MACRO_SIGNATURE = "MACRO macroName { BODY }: Creates a Macro that substitues any references for the BODY"


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

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


# TODO(map) Because the line_num in the program starts at 0 we add 1 for now.
class InvalidTokenException(Exception):
    def __init__(self, line_num, col_num, character):
        super().__init__("Invalid token.")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.character = character

    def __str__(self):
        return f"Invalid token '{self.character}' at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.character == other.character, f"{self.character, other.character}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.character == other.character


class NoTerminatorError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Line is not terminted with a semicolon.")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Line {self.line_num}:{self.col_num} must end with a semicolon."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class UnknownKeywordError(Exception):
    def __init__(self, line_num, col_num, keyword):
        super().__init__("Unknown keyword")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.keyword = keyword

    def __str__(self):
        return f"Unknown keyword '{self.keyword}' at {self.line_num}:{self.col_num} in program."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.keyword == other.keyword, f"{self.keyword, other.keyword}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.keyword == other.keyword


class InvalidVariableNameError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid variable name")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Variable name at {self.line_num}:{self.col_num} cannot start with digit."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class KeywordMisuseException(Exception):
    def __init__(self, line_num, col_num, keyword, usage):
        super().__init__("Improper use of keyword.")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.keyword = keyword
        self.usage = usage

    def __str__(self):
        return f"Improper use of '{self.keyword}' at {self.line_num}:{self.col_num} in program. \n   Sample Usage: {self.usage}"

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num} == {other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num} == {other.col_num}"
        assert self.keyword == other.keyword, f"{self.keyword} == {other.keyword}"
        assert self.usage == other.usage, f"{self.usage} == {other.usage}"
        return (self.line_num == other.line_num and self.col_num == other.col_num and self.keyword == other.keyword and self.usage == other.usage)


class TooManyArgsException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Too many args")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Too many args for keyword at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class NotEnoughArgsException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Not enough args")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Not enough args for keyword at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class InvalidArgsException(Exception):
    def __init__(self, line_num, col_num, keyword, arg_type):
        super().__init__("Invalid args")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.keyword = keyword
        self.arg_type = arg_type

    def __str__(self):
        return f"Keyword '{self.keyword}' does not support '{self.arg_type}' at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.keyword == other.keyword, f"{self.keyword, other.keyword}"
        assert self.arg_type == other.arg_type, f"{self.arg_type, other.arg_type}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.keyword == other.keyword and self.arg_type == other.arg_type


class UnclosedQuotationException(Exception):
    def __init__(self, line_num, col_num, string):
        super().__init__("Unclosed quotation")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.string = string

    def __str__(self):
        return f"Unclosed quotation mark for '{self.string}' at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.string == other.string, f"{self.string, other.string}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.string == other.string


class InvalidCharException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid char")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Invalid declaration of `char` at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class BadFormattedLogicBlock(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Badly formatted logic block")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Incorrectly formatted else statement at {self.line_num}:{self.col_num}. Cannot have code between if/else block."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class UnpairedElseError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unpaired else")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"else at {self.line_num}:{self.col_num} does not have a matching if block."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class InvalidTypeDeclarationException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid type")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Invalid type at {self.line_num}:{self.col_num}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class BufferOverflowException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Buffer overflow")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"Buffer overflow at {self.line_num}:{self.col_num}. Value too large."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class InvalidAssignmentException(Exception):
    def __init__(self, line_num, col_num, base_type, assignment_type):
        super().__init__("Invalid assignment")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.base_type = base_type
        self.assignment_type = assignment_type

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot assign a {self.base_type} with a {self.assignment_type}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.base_type == other.base_type, f"{self.base_type, other.base_type}"
        assert self.assignment_type == other.assignment_type, f"{self.assignment_type, other.assignment_type}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.base_type == other.base_type and self.assignment_type == other.assignment_type


class InvalidConcatenationException(Exception):
    def __init__(self, line_num, col_num, base_type, concat_type):
        super().__init__("Invalid concatenation")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.base_type = base_type
        self.concat_type = concat_type

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot concatenate a {self.base_type} with a {self.concat_type}."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        assert self.base_type == other.base_type, f"{self.base_type, other.base_type}"
        assert self.concat_type == other.concat_type, f"{self.concat_type, other.concat_type}"
        return self.line_num == other.line_num and self.col_num == other.col_num and self.base_type == other.base_type and self.concat_type == other.concat_type


class UnnamedFunctionException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unnamed Function")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot declare Function without a name."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num and type(self) == type(other)


class InvalidFunctionDeclarationException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid Function")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Function was declared with invalid syntax."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num and type(self) == type(other)


class InvalidMacroDeclaration(Exception):
    def __init__(self, line_num, col_num, function_name, is_ref=False):
        super().__init__("Invalid MACRO")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.function_name = function_name
        self.is_ref = is_ref

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot {'use' if self.is_ref else 'declare'} MACRO inside `{self.function_name}` method."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class UnnamedMacroException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unnamed MACRO")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot declare MACRO without a name."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class EmptyMacroException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Unnamed MACRO")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return f"{self.line_num}:{self.col_num} Cannot declare an empty MACRO."

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


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

    # TODO(map) Re-examine how this works. Need better rules around traversal
    def can_traverse_to_parent(self):
        if self.parent_node:
            return type(self.parent_node) != LogicKeywordNode and type(self.parent_node) != FunctionKeywordNode and type(self.parent_node) != FunctionReturnNode and type(self.parent_node) != LoopDownKeywordNode and type(self.parent_node) != LoopDownInclusiveKeywordNode and type(self.parent_node) != LoopUpKeywordNode and type(self.parent_node) != LoopUpInclusiveKeywordNode and type(self.parent_node) != LoopFromKeywordNode and type(self.parent_node) != LoopFromInclusiveKeywordNode
        else:
            return False


class NoOpNode(Node):
    """
    Node that functionally does nothing. This is in case I want to preserve
    data across the compilation much like with useless tokens.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, NO_OP, None)


class LeftParenNode(Node):
    """
    Basic left parenthesis node that is not tied to a function call or
    conditional block of code.
    """
    def __init__(self, token, value):
        self.token = token
        self.value = value
        super().__init__(token, HIGH)


class RightParenNode(Node):
    """
    Basic right parenthesis node that is not tied to a function call or
    conditional block of code.
    """
    def __init__(self, token, value):
        self.token = token
        self.value = value
        super().__init__(token, HIGH)


class FunctionCallLeftParenNode(NoOpNode):
    """
    Left parenthesis that is paired with the calling of a function.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token)


class FunctionCallRightParenNode(NoOpNode):
    """
    Right parenthesis that is paired with the calling of a function.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token)


class ConditionalLeftParenNode(NoOpNode):
    """
    Left parenthesis that is paired with a conditional statement.
    """
    def Left__init__(self, token):
        self.token = token
        super().__init__(token)


class ConditionalRightParenNode(NoOpNode):
    """
    Right parenthesis that is paired with a conditional statement.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token)


class FunctionBodyLeftCurlNode(Node):
    """
    Left curl brace that is paired with the function of a body
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class FunctionBodyRightCurlNode(Node):
    """
    Right parenthesis that is paired with the calling of a function.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class IfBodyLeftCurlNode(Node):
    """
    Left curl brace that is paired with the declaration of the body of an if
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class IfBodyRightCurlNode(Node):
    """
    Right curl brace that is paired with the declaration of the body of an if
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class ElseBodyLeftCurlNode(Node):
    """
    Left curl brace that is paired with the declaration of the body of an else
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class ElseBodyRightCurlNode(Node):
    """
    Right curl brace that is paired with the declaration of the body of an else
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class LoopBodyLeftCurlNode(Node):
    """
    Left curl brace that is paired with the declaration of the body of a loop
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class LoopBodyRightCurlNode(Node):
    """
    Right curl brace that is paired with the declaration of the body of a loop
    keyword.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token, LOW)


class EndOfLineNode(NoOpNode):
    """
    Node to represent the end of a line of code.
    """
    def __init__(self, token):
        self.token = token
        super().__init__(token)


class ArgSeparatorNode(Node):
    """
    Node to declare a type we can use for conditional checks. Child of NoOp as
    we don't want to do anything with it, but it is specific for separating out
    arguments in a function.
    """
    def __init__(self, token):
        super().__init__(token, LOW)


class KeywordNode(Node):
    """
    Node for keyword in the Katana language.
    """

    def __init__(self, token, value, child_node=None, parent_node=None):
        super().__init__(token, ULTRA_HIGH, parent_node)
        self.value = value
        self.child_node = child_node
        if self.child_node:
            self.child_node.parent_node = self

    def __eq__(self, other):
        child_equal = self.child_node == other.child_node
        values_equal = self.value == other.value
        return child_equal and values_equal and super().__eq__(other)

    def __repr__(self):
        if self.child_node:
            return f"({self.value}({self.child_node}))"
        else:
            return f"({self.value})"


class FunctionDecSeparatorNode(Node):
    """
    Node for holding a separator in the function declartion. This is the "::"
    operator and really only serves to make sure the function syntax is correct
    as part of the rule checking
    """
    def __init__(self, token):
        super().__init__(token, LOW)
        self.token = token

    def __eq__(self, other):
        return self.token == other.token


class FunctionDecLeftParenNode(Node):
    """
    Simple node for left parens as they are used in function declaration.
    """
    def __init__(self, token):
        super().__init__(token, LOW)
        self.token = token

    def __eq__(self, other):
        return self.token == other.token


class FunctionDecRightParenNode(Node):
    """
    Simple node for right parens as they are used in function declaration.
    """
    def __init__(self, token):
        super().__init__(token, LOW)
        self.token = token

    def __eq__(self, other):
        return self.token == other.token


class FunctionNode(Node):
    """
    Node for all things function based. Key difference between this and keyword
    node is that the function node has a list of args but a keyword only has
    a single childe node.
    """
    def __init__(self, token, value, function_name=None, function_args=[], function_return_type=None, function_body=None, parent_node=None):
        super().__init__(token, ULTRA_HIGH, parent_node)
        self.value = value
        self.function_name = function_name
        self.function_return_type = function_return_type
        self.function_body = function_body
        self.function_args = function_args
        for node in function_args:
            node.parent_node = self

    def __eq__(self, other):
        # TODO(map) Make this equal better
        args_equal = self.function_args == other.function_args
        return args_equal and type(self) == type(other) and super().__eq__(other)

    def __repr__(self):
        arg_nodes = "["
        if self.function_args:
            for node in self.function_args:
                arg_nodes += node.__repr__() + ","
        arg_nodes += "]"
        body_nodes = "["
        if self.function_body:
            for node in self.function_body:
                body_nodes += node.__repr__() + ","
        body_nodes += "]"

        return f"({self.value}, {self.function_name}, {self.function_return_type}, {arg_nodes}, {body_nodes})"


class FunctionKeywordNode(Node):
    """
    More specialized node for Function keywords vs other types of keywords.
    """
    def __init__(self, token, value, parent_node=None, arg_nodes=None):
        super().__init__(token, HIGH, parent_node)
        self.value = value
        if arg_nodes:
            self.arg_nodes = arg_nodes

    def __eq__(self, other):
        return type(self) == type(other) and super().__eq__(other)

    def __repr__(self):
        return f"({self.value}, {self.arg_nodes})"


class FunctionReferenceNode(Node):
    """
    Class for holding a call to a function
    """
    def __init__(self, token, value, function_args=[], parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.function_args = function_args

    def __eq__(self, other):
        return type(self) == type(other) and self.function_args == other.function_args and super().__eq__(other)

    def __repr__(self):
        # TODO(MAP) This may get confusing with the funtion declaration in how it reads.
        return f"({self.value}, {self.function_args})"


class FunctionNameNode(Node):
    """
    Node for holding the name of the user defined function.
    """
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, parent_node)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and super().__eq__(other)

    def __repr__(self):
        return f"{self.value}"


class FunctionArgNode(Node):
    """
    Node for holding the definition of a function argument
    """
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


class FunctionArgSeparatorNode(Node):
    """
    Node for holding the separator of function arguments
    """
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


class FunctionArgTypeNode(Node):
    """
    Node for holding the type definition of a function argument
    """
    def __init__(self, token, value, fn_arg_name=None, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.fn_arg_name = fn_arg_name
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        fn_arg_names_equal = self.fn_arg_name == other.fn_arg_name
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
            assert False, f"Value {self.value} != {other.value}"
        if not fn_arg_names_equal and raise_assertion_flag:
            assert False, f"Value {self.fn_arg_name} != {other.fn_arg_name}"
        return (types_equal and values_equal and fn_arg_names_equal)

    def __repr__(self):
        return f"({self.value}({self.fn_arg_name}))"


class FunctionArgReferenceNode(Node):
    """
    Node for holding the reference of a function argument
    """
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


class FunctionReturnTypeNode(Node):
    """
    Node for holding the return type of a function
    """
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


class FunctionReturnNode(Node):
    """
    Node for holding the return statement of a function
    """
    def __init__(self, token, value, return_body=None, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.return_body = return_body
        self.parent_node = parent_node

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        returns_equal = self.return_body == other.return_body
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
            assert False, f"Value {self.value} != {other.value}"
        if not returns_equal and raise_assertion_flag:
            assert False, f"Returns {self.return_body} != {other.return_body}"
        return (types_equal and values_equal and returns_equal)

    def __repr__(self):
        return f"({self.value}, {self.return_body})"


class LogicKeywordNode(KeywordNode):
    """
    More specialized node for Logic keywords vs other types of keywords.
    """
    def __init__(self, token, value, child_node=None, parent_node=None, true_side=None, false_side=None):
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
    def __init__(self, token, value, child_node=None, parent_node=None):
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
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        self.start_value = 0
        if self.child_node:
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
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        if self.child_node:
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
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        if child_node:
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


class LoopUpInclusiveKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `iLoopUp` keyword specifically.
    """
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        self.start_value = 0
        if self.child_node:
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


class LoopDownInclusiveKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `iLoopDown` keyword specifically.
    """
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        if self.child_node:
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


class LoopFromInclusiveKeywordNode(LoopKeywordNode):
    """
    Specialized node for the `iLoopFrom` keyword specifically.
    """
    def __init__(self, token, value, child_node=None, parent_node=None, loop_body=None):
        super().__init__(token, value, child_node, parent_node, loop_body)

        # Because this is loop up we will always loop from 0 to the end value.
        if child_node:
            self.start_value = child_node.left_side.value
            self.end_value = child_node.right_side.value

        if loop_body:
            for node in loop_body:
                node.parent_node = self

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        loop_body_equal = self.loop_body == other.loop_body
        if not loop_body_equal:
            assert False, f"Loop bodies not equal for {self}"
        return types_equal and loop_body_equal and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()



class LoopIdxKeywordNode(Node):
    """
    Specialized node for accessing the index of the current loop
    """
    def __init__(self, token, value, parent_node=None):
        super().__init__(token, parent_node)
        self.value = value

    def __eq__(self, other):
        types_equal = type(self) == type(other)
        return types_equal and super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

    def __repr__(self):
        return f"({self.value})"


class StartNode(Node):
    """
    Special node that represents the `main` keyword that starts the program.
    """
    def __init__(self, token, value, children_nodes=[]):
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

    def get_children_nodes(self):
        return None


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

    def get_children_nodes(self):
        return None


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
        if self.left_side:
            self.left_side.parent_node = self
        if self.right_side:
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
            # TODO(map) This doesn't give a clear explanation when one of the
            # values aren't equal. Consider a better error message.
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
            assert self.parent_node.token == other.parent_node.token, f"Token comparison: {self.parent_node.token} != {other.parent_node.token}"
            assert self.parent_node.priority == other.parent_node.priority, f"Priority comparison: {self.parent_node.priority} != {other.parent_node.priority}"
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

    def get_children_nodes(self):
        if not self.left_side and not self.right_side:
            return None
        elif not self.left_side and self.right_side:
            return [self.right_side]
        elif not self.right_side and self.left_side:
            return [self.left_side]
        else:
            return [self.left_side, self.right_side]


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

    def get_children_nodes(self):
        return [self.left_side, self.right_side]


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

    def get_children_nodes(self):
        return None


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
    def __init__(self, token, value, is_const, parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.parent_node = parent_node
        self.is_const = is_const

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

    def get_children_nodes(self):
        return None


class MacroNode(Node):
    def __init__(self, token, value, name_node=None, children_nodes=[], parent_node=None):
        super().__init__(token, LOW, parent_node)
        self.value = value
        self.name_node = name_node
        self.children_nodes = children_nodes
        self.parent_node = parent_node

        for node in self.children_nodes:
            node.parent_node = self


    def __eq__(self, other):
        types_equal = type(self) == type(other)
        values_equal = self.value == other.value
        children_equal = self.children_nodes == other.children_nodes
        if not types_equal and raise_assertion_flag:
            assert False, f"Type {type(self)} != {type(other)}"
        if not values_equal and raise_assertion_flag:
            assert False, f"Value {self.value} != {other.value}"
        return (types_equal and values_equal and children_equal)

    def __repr__(self):
        return f"({self.value}, {self.name_node}, [{self.children_nodes}])"

    def get_children_nodes(self):
        return self.children_nodes


class MacroNameNode(Node):
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


class MacroReferenceNode(Node):
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

    def has_next_line(self):
        return self.curr_line + 1 < self.line_count + 1


########
# UTILS
########
def print_verbose_message(message):
    if verbose_flag:
        print(message)


def print_exception_message(program, position, exception):
    start_line = exception.line_num - 3 if exception.line_num - 3 >= 0 else 0
    for line in program[start_line:exception.line_num]:
        print(line)
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
        self.macro_name_list = []
        self.variable_name_list = []
        self.unpaired_parens = 0
        self.misused_keywords = 0
        self.comment_index = -1
        # Function tracking information. This is needed because we need to track
        # function args as they are related to their respective functions. This
        # means that `x` in `add` shouldn't cross pollinate with `x` in `print`
        # Without this `x` could really mean anything.
        self.in_function_declaration = False
        self.fn_left_paren_set = False
        self.curr_function_name = None
        self.function_args = {}

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
                # No longer in function declaration so alphas are variables again.
                self.in_function_declaration = False
                return Token(LEFT_CURL_BRACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == '(':
                if self.in_function_declaration:
                    self.fn_left_paren_set = True
                return Token(LEFT_PAREN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == '}':
                return Token(RIGHT_CURL_BRACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == ')':
                if not self.in_function_declaration:
                    self.check_for_valid_termination(character)
                if self.in_function_declaration:
                    self.fn_left_paren_set = False
                return Token(RIGHT_PAREN_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, VERY_HIGH)
            elif character == ';':
                return Token(EOL_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character == '\'':
                return self.generate_char_token()
            elif character == '"':
                return self.generate_string_token()
            elif character == ".":
                return self.handle_dot_character()
            elif character == "," and not self.in_function_declaration:
                return Token(COMMA_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character == "," and self.in_function_declaration:
                return Token(FUNCTION_ARG_SEPARATOR_TYPE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character.isalpha():
                token = self.generate_keyword_token()
                if token.ttype == FUNCTION_ARG_TOKEN_TYPE and not self.fn_left_paren_set:
                    raise InvalidFunctionDeclarationException(token.row, token.col)
                else:
                    return token
            elif character == ':' and self.program.get_next_char() == ':':
                return self.handle_function_separator()
            elif character == ':' and self.program.get_next_char() != ':':  # Do we care about a single colon by itself?
                return Token(COLON_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character == "\n":
                self.check_for_valid_termination(character)
                return Token(NEW_LINE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            elif character.isspace():  # Never care about spaces
                return Token(SPACE_TOKEN_TYPE, self.program.curr_col, self.program.curr_line, character, LOW)
            else:
                raise InvalidTokenException(self.program.curr_line, self.program.curr_col, character)
        except InvalidVariableNameError as ivne:
            print_exception_message(self.program.lines, self.program.curr_col, ivne)
            sys.exit()
        except NoTerminatorError as nte:
            print_exception_message(self.program.lines, self.program.curr_col, nte)
            sys.exit()
        except InvalidTokenException as ite:
            print_exception_message(self.program.lines, self.program.curr_col, ite)
            sys.exit()
        except UnknownKeywordError as uke:
            print_exception_message(self.program.lines, self.program.curr_col, uke)
            sys.exit()
        except UnclosedQuotationException as uqe:
            print_exception_message(self.program.lines, self.program.curr_col, uqe)
            sys.exit()
        except InvalidCharException as ice:
            print_exception_message(self.program.lines, self.program.curr_col, ice)
            sys.exit()
        except InvalidFunctionDeclarationException as ifde:
            print_exception_message(self.program.lines, self.program.curr_col, ifde)
            sys.exit()

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
                left_paren_has_keyword = token.value in LOGIC_KEYWORDS or token.value == MAIN
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

        if keyword in FUNCTION_KEYWORDS + VARIABLE_KEYWORDS + LOGIC_KEYWORDS and not self.in_function_declaration:
            if keyword == IF:
                self.if_idx_list.append(len(self.token_list))
            elif keyword == ELSE:
                self.else_idx_list.append(len(self.token_list))
            return Token(KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, ULTRA_HIGH)
        elif keyword == MACRO:
            return Token(MACRO_KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, ULTRA_HIGH)
        elif len(self.token_list) > 0 and self.token_list[-1].value in VARIABLE_KEYWORDS:
            self.variable_name_list.append(keyword)
            return Token(VARIABLE_NAME_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif len(self.token_list) > 0 and self.token_list[-1].value == MACRO:
            self.macro_name_list.append(keyword)
            return Token(MACRO_NAME_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif keyword in self.macro_name_list:
            return Token(MACRO_REFERENCE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif keyword in self.variable_name_list:
            return Token(VARIABLE_REFERENCE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif keyword in ["true", "false"]:
            return Token(BOOLEAN_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, LOW)
        elif keyword == FN:
            return Token(FUNCTION_KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif keyword == "return":
            return Token(FUNCTION_RETURN_KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, HIGH)
        elif len(self.token_list) > 0 and self.token_list[-1].value == FN:
            self.in_function_declaration = True
            self.curr_function_name = keyword
            self.function_args[self.curr_function_name] = {}
            return Token(FUNCTION_NAME_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif self.in_function_declaration and keyword not in VARIABLE_KEYWORDS and keyword != "nil":
            self.function_args[self.curr_function_name].update({keyword: ""})
            return Token(FUNCTION_ARG_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif self.in_function_declaration and keyword in VARIABLE_KEYWORDS and self.token_list[-1].ttype != FUNCTION_SEPARATOR_TOKEN_TYPE:
            self.function_args[self.curr_function_name].update({self.token_list[-1].value: keyword})
            return Token(FUNCTION_ARG_TYPE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif self.in_function_declaration and keyword in VARIABLE_KEYWORDS and self.token_list[-1].ttype == FUNCTION_SEPARATOR_TOKEN_TYPE:
            return Token(FUNCTION_RETURN_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif self.in_function_declaration and keyword == "nil":
            return Token(FUNCTION_RETURN_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif keyword in self.function_args.get(self.curr_function_name, {}):
            return Token(FUNCTION_ARG_REFERENCE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, HIGH)
        elif keyword in self.function_args.keys():
            return Token(FUNCTION_REFERENCE_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, VERY_HIGH)
        elif keyword == "idx":
            return Token(LOOP_INDEX_KEYWORD_TOKEN_TYPE, original_pos, self.program.curr_line, keyword, HIGH)
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
            print_exception_message(self.program.lines, self.program.curr_col, InvalidTokenException(self.program.curr_line, self.program.curr_col, dot_operator))
            sys.exit()

    def handle_equal_operator(self):
        equal_idx = self.program.curr_col
        self.program.advance_character()
        return Token(EQUAL_TOKEN_TYPE, equal_idx, self.program.curr_line, "==", HIGH)

    def handle_function_separator(self):
        fn_idx = self.program.curr_col
        self.program.advance_character()
        return Token(FUNCTION_SEPARATOR_TOKEN_TYPE, fn_idx, self.program.curr_line, "::", VERY_HIGH)

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
            print_exception_message(self.program.lines, paren_error_col, upe)
            sys.exit()

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
                        print_exception_message(self.program.lines, err_token.row, UnpairedElseError(err_token.row, err_token.col))
                        sys.exit()
                        # raise UnpairedElseError(err_token.row, err_token.col)
                # All other if/else pairs matched so the final else must be
                # the problem
                err_token = self.token_list[self.else_idx_list[-1]]
                print_exception_message(self.program.lines, err_token.row, UnpairedElseError(err_token.row, err_token.col))
                sys.exit()

        # If/else blocks all match, make sure there is nothing between the end
        # of an `if` block and the start of an `else` block
        filtered_token_list = list(filter(lambda token: (token.ttype != NEW_LINE_TOKEN_TYPE), self.token_list))
        for idx, token in enumerate(filtered_token_list):
            # TODO(map) There's a fun bug here where if there is a string with
            # the value of "else" there will be an exception message raised.
            if token.value == ELSE and filtered_token_list[idx - 1].ttype != RIGHT_CURL_BRACE_TOKEN_TYPE:
                print_exception_message(self.program.lines, token.row, BadFormattedLogicBlock(token.row, 0))
                sys.exit()


########
# PARSER
########
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.has_next_token = True
        self.curr_token_pos = -1
        self.main_node = None
        self.variable_to_type_map = {}
        self.macros = {}
        self.macro_reference_set = False
        self.node_list = []
        self.if_else_list = []
        self.left_paren_func_call_set = False
        self.in_function_body = False
        self.current_if_node = None
        self.fn_name_ret_type_map = {}

    def get_nodes(self):
        ret_nodes = []
        ret_nodes.extend(self.node_list)
        if self.main_node:
            ret_nodes.append(self.main_node)
        return ret_nodes

    def parse(self):
        root_node = None
        # TODO(map) Figure out what I want to actually do here. Currently I am
        # choosing to not advance to parser because the method being used will
        # parse to the end of the line and go to the next token. One possible
        # solution could be to have a method that handles building a top level
        # AST that would not process the EOL token.
        should_skip_advance = False
        while self.has_next_token:
            if should_skip_advance:
                should_skip_advance = False
                pass
            else:
                self.advance_token()
            try:
                if self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == MAIN:
                    self.node_list.append(self.process_main_token(self.curr_token))
                elif self.curr_token.ttype == FUNCTION_KEYWORD_TOKEN_TYPE and self.curr_token.value == FN:
                    self.node_list.append(self.process_fn_token(self.curr_token))
                    should_skip_advance = True
                elif self.curr_token.ttype == MACRO_KEYWORD_TOKEN_TYPE and self.curr_token.value == MACRO:
                    self.node_list.append(self.process_macro_token(self.curr_token))
                    should_skip_advance = True
                elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value in VARIABLE_KEYWORDS:
                    dec_node = self.process_token()
                    self.node_list.append(self.build_var_dec_line_ast(dec_node))
                    should_skip_advance = True
                elif self.curr_token.ttype == EOF_TOKEN_TYPE:
                    # We've reached the end of the token list
                    self.has_next_token = False
                else:
                    assert False, f"Token {self.curr_token.value} is not one of the {len(TOP_LEVEL_TOKENS)} top level tokens."
            except KeywordMisuseException as kme:
                print_exception_message(program_lines, kme.col_num, kme)
                sys.exit()
            except TooManyArgsException as tmae:
                print_exception_message(program_lines, tmae.col_num, tmae)
                sys.exit()
            except BufferOverflowException as boe:
                print_exception_message(program_lines, boe.col_num, boe)
                sys.exit()
            except InvalidArgsException as iae:
                print_exception_message(program_lines, iae.col_num, iae)
                sys.exit()
            except InvalidAssignmentException as iaae:
                print_exception_message(program_lines, iaae.col_num, iaae)
                sys.exit()
            except InvalidConcatenationException as ice:
                print_exception_message(program_lines, ice.col_num, ice)
                sys.exit()
            except InvalidTypeDeclarationException as itde:
                print_exception_message(program_lines, itde.col_num, itde)
                sys.exit()
            except InvalidMacroDeclaration as imd:
                print_exception_message(program_lines, imd.col_num, imd)
                sys.exit()
            except EmptyMacroException as eme:
                print_exception_message(program_lines, eme.col_num, eme)
                sys.exit()
            except UnnamedFunctionException as ufe:
                print_exception_message(program_lines, ufe.col_num, ufe)
                sys.exit()
            except InvalidFunctionDeclarationException as ifde:
                print_exception_message(program_lines, ifde.col_num, ifde)
                sys.exit()

    def advance_token(self):
        # Ensure we can advance
        if self.curr_token_pos + 1 < len(self.token_list):
            self.curr_token_pos += 1
            self.curr_token = self.token_list[self.curr_token_pos]

    def peek_next_token(self):
        return self.token_list[self.curr_token_pos + 1]

    def get_prev_token(self):
        return self.token_list[self.curr_token_pos - 1]

    def process_main_token(self, main_token):
        """Signature is `main() { BODY };`"""
        # Create the main node with no children. They will be added later in
        # this method.
        main_node = self.process_token()

        # Confirm the left paren is right after the main keyword
        root_node = self.process_token()
        if not isinstance(root_node, FunctionCallLeftParenNode):
            raise KeywordMisuseException(main_token.row, main_token.col, main_token.value, MAIN_SIGNATURE)

        # Confirm the right paren closes the left.
        root_node = self.process_token()
        if not isinstance(root_node, FunctionCallRightParenNode):
            raise KeywordMisuseException(main_token.row, main_token.col, main_token.value, MAIN_SIGNATURE)

        # Confirm left curl brack is present.
        root_node = self.process_token()
        if not isinstance(root_node, FunctionBodyLeftCurlNode):
            raise KeywordMisuseException(main_token.row, main_token.col, main_token.value, MAIN_SIGNATURE)

        # Flag for determining if we are at end of the main loop
        end_of_main = False

        # Process the first token since we should anyways.
        processed_node = self.process_token()

        # Loop through the entire body of the main function.
        # while type(processed_node) != FunctionBodyRightCurlNode:
        while not end_of_main:
            # Ran into a NoOp after a line has been processed. This should
            # really only happen for a comment after a line of code.
            if type(processed_node) in [NoOpNode, EndOfLineNode]:
                # Process the next token after the NoOp
                processed_node = self.process_token()
                end_of_main = type(processed_node) == FunctionBodyRightCurlNode
                continue

            if self.macro_reference_set:
                for node in processed_node:
                    main_node.children_nodes.append(node)
                    node.parent_node = main_node
                self.macro_reference_set = False
            elif type(processed_node) == MacroNode:
                raise InvalidMacroDeclaration(main_token.row, main_token.col, main_token.value)
            else:
                line_ast = self.build_line_ast(processed_node)
                main_node.children_nodes.append(line_ast)


            # Process the next token after the EOL
            processed_node = self.process_token()
            # Determine if we have reached the end of the main func body
            if type(processed_node) == FunctionBodyRightCurlNode:
                end_of_main = True

        # Set the childrens parents to the main node
        for child_node in main_node.children_nodes:
            child_node.parent_node = main_node

        return main_node

    def process_fn_token(self, fn_token):
        # Create the fn node with no children. They will be added later in
        # this method.
        fn_node = self.process_token()
        self.if_else_list.append(fn_node)

        # Make sure the next node is the name of the function.
        fn_name_node = self.process_token()
        if not isinstance(fn_name_node, FunctionNameNode):
            raise UnnamedFunctionException(fn_token.row, fn_token.col)

        # Next check for a function args separator node
        processed_node = self.process_token()
        if not isinstance(processed_node, FunctionDecSeparatorNode):
            raise InvalidFunctionDeclarationException(fn_token.row, fn_token.col)

        # Check for left paren around params
        processed_node = self.process_token()
        if not isinstance(processed_node, FunctionDecLeftParenNode):
            raise InvalidFunctionDeclarationException(fn_token.row, fn_token.col)

        # Check for any parameters that are being declared on the function.
        func_arg_params = []
        processed_node = self.process_token()
        name_node = None
        type_node = None
        if not isinstance(processed_node, FunctionDecRightParenNode):
            # There are parameters and they need to be parsed
            while not isinstance(processed_node, FunctionDecRightParenNode):
                if isinstance(processed_node, FunctionArgNode):
                    name_node = processed_node
                elif isinstance(processed_node, FunctionArgTypeNode):
                    type_node = processed_node
                    name_node.parent_node = type_node
                    type_node.fn_arg_name = name_node
                    self.variable_to_type_map[name_node.value] = type_node.value
                elif isinstance(processed_node, FunctionArgSeparatorNode):
                    func_arg_params.append(type_node)
                    name_node = None
                    type_node = None
                else:
                    assert False, "Unsure how to handle node in func args"
                processed_node = self.process_token()
        
        # TODO(map) This is not great but it's one way to ensure we add the
        # final node if it isn't already added
        if len(func_arg_params) > 0 and func_arg_params[-1] != type_node:
            func_arg_params.append(type_node)

        # Check for the right closing parenthesis on the method param
        # declaration. No need to process a token though as the loop above has
        # already processed the node right after the last param.
        if not  isinstance(processed_node, FunctionDecRightParenNode):
            raise InvalidFunctionDeclarationException(fn_token.row, fn_token.col)

        # Next check for a function args separator node
        processed_node = self.process_token()
        if not isinstance(processed_node, FunctionDecSeparatorNode):
            raise InvalidFunctionDeclarationException(fn_token.row, fn_token.col)

        # Get the return type node from the function declaration
        return_type_node = self.process_token()
        if not isinstance(return_type_node, FunctionReturnTypeNode):
            assert False, "TODO(map) Raise the appropriate exception"

        # Get the left curl brace to start the function body definition
        processed_node = self.process_token()
        if not isinstance(processed_node, FunctionBodyLeftCurlNode):
            assert False, "TODO(map) Raise the appropriate exception"

        # Flag for determining if we are at end of the loop
        end_of_function = False

        # Process the first node as there should always be a line of work in a
        # method regardless
        processed_node = self.process_token()
        fn_body_list = []
        while not end_of_function:
            # Ran into a NoOp so we just need to process the next node
            if type(processed_node) == NoOpNode:
                # Process the next token after the NoOp
                processed_node = self.process_token()
                end_of_function = type(processed_node) == FunctionBodyRightCurlNode
                continue

            line_ast = self.build_line_ast(processed_node)
            fn_body_list.append(line_ast)

            # Process the next token after the EOL
            processed_node = self.process_token()
            # Determine if we have reached the end of the main func body
            if type(processed_node) == FunctionBodyRightCurlNode:
                end_of_function = True

        # Build up the complete function node now that we have all the different
        # components needed.
        # Set the function name node
        fn_node.function_name = fn_name_node
        fn_name_node.parent_node = fn_node

        # Set the function arg nodes
        fn_node.function_args = func_arg_params
        for node in func_arg_params:
            node.parent_node = fn_node

        # Set the function return type node
        fn_node.function_return_type = return_type_node
        return_type_node.parent_node = fn_node

        # Set the function body nodes
        fn_node.function_body = fn_body_list
        for node in fn_body_list:
            node.parent_node = fn_node

        self.fn_name_ret_type_map[fn_node.function_name.value] = fn_node.function_return_type.value
        return fn_node

    def process_macro_token(self, macro_token):
        """Signature is `MACRO macro_name { BODY };`"""
        # Create the main node with no children. They will be added later in
        # this method.
        macro_node = self.process_token()

        # Confirm the macro name is after the macro keyword
        macro_name_node = self.process_token()
        if not isinstance(macro_name_node, MacroNameNode):
            raise KeywordMisuseException(macro_token.row, macro_token.col, macro_token.value, MACRO_SIGNATURE)
        macro_node.name_node = macro_name_node
        macro_name_node.parent_node = macro_node
 
        # Confirm the macro name is after the macro keyword
        root_node = self.process_token()
        if not isinstance(root_node, FunctionBodyLeftCurlNode):
            raise KeywordMisuseException(macro_token.row, macro_token.col, macro_token.value, MACRO_SIGNATURE)

        # Flag for determining if we are at end of the main loop
        end_of_macro = False

        # Process the first token since we should anyways.
        processed_node = self.process_token()

        # Confirm the node is not a right curl brace meaning an empty macro
        if isinstance(processed_node, FunctionBodyRightCurlNode):
            raise EmptyMacroException(macro_token.row, macro_token.col)

        # Loop through the entire body of the main function.
        # while type(processed_node) != FunctionBodyRightCurlNode:
        while not end_of_macro:
            line_ast = self.build_line_ast(processed_node)
            macro_node.children_nodes.append(line_ast)

            # Process the next token after the EOL
            processed_node = self.process_token()
            # Determine if we have reached the end of the main func body
            if type(processed_node) == FunctionBodyRightCurlNode:
                end_of_macro = True

        # Set the childrens parents to the main node
        for child_node in macro_node.children_nodes:
            child_node.parent_node = macro_node

        self.macros[macro_name_node.value] = macro_node.children_nodes

        return macro_node

    def build_line_ast(self, processed_node):
        if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
            line_ast = self.build_print_ast(processed_node)
        elif type(processed_node) == FunctionKeywordNode and processed_node.value == CHAR_AT:
            line_ast = self.build_char_at_line_ast(processed_node)
        elif type(processed_node) == FunctionKeywordNode and processed_node.value == UPDATE_CHAR:
            line_ast = self.build_update_char_line_ast(processed_node)
        elif type(processed_node) == FunctionKeywordNode and processed_node.value == COPY_STR:
            line_ast = self.build_copy_str_line_ast(processed_node)
        # "const" can only be declared on a variable right now. This
        # makes it safe to call the build var ast method even if const
        # is the value of the currently processed node as we know a var
        # declaration will follow
        elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
            line_ast = self.build_var_dec_line_ast(processed_node)
        elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
            line_ast = self.build_if_conditional_line_ast(processed_node)
            # Mark the current if node so we can pair it with an else if needed
            self.current_if_node = processed_node
        elif type(processed_node) == LoopUpKeywordNode:
            line_ast = self.build_loop_up_line_ast(processed_node)
        elif type(processed_node) == LoopUpInclusiveKeywordNode:
            line_ast = self.build_loop_up_line_ast(processed_node)
        elif type(processed_node) == LoopDownKeywordNode:
            line_ast = self.build_loop_down_line_ast(processed_node)
        elif type(processed_node) == LoopDownInclusiveKeywordNode:
            line_ast = self.build_loop_down_line_ast(processed_node)
        elif type(processed_node) == LoopFromKeywordNode:
            line_ast = self.build_loop_from_line_ast(processed_node)
        elif type(processed_node) == LoopFromInclusiveKeywordNode:
            line_ast = self.build_loop_from_line_ast(processed_node)
        elif type(processed_node) == FunctionReturnNode:
            line_ast = self.build_return_statement(processed_node)
        elif type(processed_node) == FunctionReferenceNode:
            line_ast = self.build_func_reference(processed_node)
        else:
            line_ast = self.build_non_keyword_line_ast(processed_node)
            # TODO(map) Be aware of this warning.
            # print("WARNING: There may be a problem in building a non-keyword line.")
        return line_ast

    def process_token(self):
        node = None
        if self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == MAIN:
            node = StartNode(self.curr_token, self.curr_token.value, [])
        elif self.curr_token.ttype == MACRO_KEYWORD_TOKEN_TYPE:
            node = MacroNode(self.curr_token, self.curr_token.value, children_nodes=[])
        elif self.curr_token.ttype == FUNCTION_KEYWORD_TOKEN_TYPE:
            node = FunctionNode(self.curr_token, self.curr_token.value, [])
        elif self.curr_token.ttype == LEFT_PAREN_TOKEN_TYPE:
            # Currently working on keyword
            if self.get_prev_token().ttype == KEYWORD_TOKEN_TYPE and self.get_prev_token().value not in [IF, ELSE]:
                node = FunctionCallLeftParenNode(self.curr_token)
                self.left_paren_func_call_set = True
            # Working on a function call
            elif self.get_prev_token().ttype == FUNCTION_REFERENCE_TOKEN_TYPE:
                node = FunctionCallLeftParenNode(self.curr_token)
                self.left_paren_func_call_set = True
            # Working on a function declaration
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == FunctionNode:
                node = FunctionDecLeftParenNode(self.curr_token)
            # Currently in an IF block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == IF:
                node = ConditionalLeftParenNode(self.curr_token)
            # This is a paren that is not linked to any key operations like an
            # if/else block or a function call.
            else:
                node = LeftParenNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == RIGHT_PAREN_TOKEN_TYPE:
            # Currently working on a function
            if self.left_paren_func_call_set:
                node = FunctionCallRightParenNode(self.curr_token)
                self.left_paren_func_call_set = False
            # Working on a function declaration
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == FunctionNode:
                node = FunctionDecRightParenNode(self.curr_token)
                self.if_else_list.pop()
            # Currently in an "if" block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == IF:
                node = ConditionalRightParenNode(self.curr_token)
            # This is a paren that is not linked to any key operations like an
            # if/else block or a function call.
            else:
                node = RightParenNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == LEFT_CURL_BRACE_TOKEN_TYPE:
            # Currently working on a loop block
            if len(self.if_else_list) > 0 and type(self.if_else_list[-1]) in [LoopUpKeywordNode, LoopDownKeywordNode, LoopFromKeywordNode, LoopUpInclusiveKeywordNode, LoopDownInclusiveKeywordNode, LoopFromInclusiveKeywordNode]:
                node = LoopBodyLeftCurlNode(self.curr_token)
            # Currently in an "if" block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == IF:
                node = IfBodyLeftCurlNode(self.curr_token)
            # Currently in an "else" block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == ELSE:
                node = ElseBodyLeftCurlNode(self.curr_token)
            # There is no if/else combination we are currently processing
            else:
                node = FunctionBodyLeftCurlNode(self.curr_token)
        elif self.curr_token.ttype == RIGHT_CURL_BRACE_TOKEN_TYPE:
            # Currently working on a loop block
            if len(self.if_else_list) > 0 and type(self.if_else_list[-1]) in [LoopUpKeywordNode, LoopDownKeywordNode, LoopFromKeywordNode, LoopUpInclusiveKeywordNode, LoopDownInclusiveKeywordNode, LoopFromInclusiveKeywordNode]:
                node = LoopBodyRightCurlNode(self.curr_token)
                self.if_else_list.pop()
            # Currently in an "if" block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == IF:
                node = IfBodyRightCurlNode(self.curr_token)
                # Remove the "if" node because we have finished processing it.
                self.if_else_list.pop()
            # Currently in an "else" block of logic.
            elif len(self.if_else_list) > 0 and type(self.if_else_list[-1]) == LogicKeywordNode and self.if_else_list[-1].value == ELSE:
                node = ElseBodyRightCurlNode(self.curr_token)
                # Remove the "else" node because we have finished processing it.
                self.if_else_list.pop()
            # There is no if/else combination we are currently processing
            else:
                node = FunctionBodyRightCurlNode(self.curr_token)
        elif self.curr_token.ttype == NUM_TOKEN_TYPE:
            node = NumberNode(self.curr_token, self.curr_token.value, None)
        elif self.curr_token.ttype == CHARACTER_TOKEN_TYPE:
            node = CharNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == STRING_TOKEN_TYPE:
            node = StringNode(self.curr_token, self.curr_token.value, None)
        elif self.curr_token.ttype in [PLUS_TOKEN_TYPE, MINUS_TOKEN_TYPE]:
            node = PlusMinusNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype in [MULTIPLY_TOKEN_TYPE, DIVIDE_TOKEN_TYPE]:
            node = MultiplyDivideNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == COMMENT_TOKEN_TYPE:
            node = NoOpNode(self.curr_token)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value in [PRINT, PRINTL, CHAR_AT, UPDATE_CHAR, COPY_STR]:
            node = FunctionKeywordNode(self.curr_token, self.curr_token.value, [])
        elif self.curr_token.ttype == MACRO_NAME_TOKEN_TYPE:
            node = MacroNameNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_NAME_TOKEN_TYPE:
            node = FunctionNameNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value in VARIABLE_KEYWORDS:
            node = VariableKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == VARIABLE_NAME_TOKEN_TYPE:
            is_const = self.token_list[self.curr_token_pos - 2].value ==  CONST
            node = VariableNode(self.curr_token, self.curr_token.value, is_const, None)
        elif self.curr_token.ttype == VARIABLE_REFERENCE_TOKEN_TYPE:
            node = VariableReferenceNode(self.curr_token, self.curr_token.value, None)
        elif self.curr_token.ttype == MACRO_REFERENCE_TOKEN_TYPE:
            node = copy.deepcopy(self.macros[self.curr_token.value])
            self.macro_reference_set = True
        elif self.curr_token.ttype == ASSIGNMENT_TOKEN_TYPE:
            node = AssignmentNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == BOOLEAN_TOKEN_TYPE:
            node = BooleanNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value in [IF, ELSE]:
            node = LogicKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == LOOP_UP:
            node = LoopUpKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == I_LOOP_UP:
            node = LoopUpInclusiveKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == LOOP_DOWN:
            node = LoopDownKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == I_LOOP_DOWN:
            node = LoopDownInclusiveKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == LOOP_FROM:
            node = LoopFromKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == KEYWORD_TOKEN_TYPE and self.curr_token.value == I_LOOP_FROM:
            node = LoopFromInclusiveKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == LOOP_INDEX_KEYWORD_TOKEN_TYPE:
            node = LoopIdxKeywordNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == RANGE_INDICATION_TOKEN_TYPE:
            node = RangeNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype in [EQUAL_TOKEN_TYPE, GREATER_THAN_TOKEN_TYPE, LESS_THAN_TOKEN_TYPE]:
            node = CompareNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == COMMA_TOKEN_TYPE:
            node = ArgSeparatorNode(self.curr_token)
        elif self.curr_token.ttype == FUNCTION_SEPARATOR_TOKEN_TYPE:
            node = FunctionDecSeparatorNode(self.curr_token)
        elif self.curr_token.ttype == FUNCTION_ARG_TOKEN_TYPE:
            node = FunctionArgNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_ARG_TYPE_TOKEN_TYPE:
            node = FunctionArgTypeNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_ARG_SEPARATOR_TYPE_TOKEN_TYPE:
            node = FunctionArgSeparatorNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_RETURN_TOKEN_TYPE:
            node = FunctionReturnTypeNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_RETURN_KEYWORD_TOKEN_TYPE:
            node = FunctionReturnNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_ARG_REFERENCE_TOKEN_TYPE:
            node = FunctionArgReferenceNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == FUNCTION_REFERENCE_TOKEN_TYPE:
            node = FunctionReferenceNode(self.curr_token, self.curr_token.value)
        elif self.curr_token.ttype == EOL_TOKEN_TYPE:
            node = EndOfLineNode(self.curr_token)
        else:
            assert False, f"Unknown token type {self.curr_token.ttype}"

        self.advance_token()
        return node

    def build_non_keyword_line_ast(self, start_node):
        node_list = [start_node]

        processed_node = self.process_token()
        while type(processed_node) != EndOfLineNode:
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [CHAR_AT, UPDATE_CHAR]:
                node_list.append(self.build_char_at_line_ast(processed_node))
            else:
                node_list.append(processed_node)
            processed_node = self.process_token()

        return self.build_ast_from_node_list(node_list)

    def build_print_ast(self, print_node):
        processed_node = self.process_token()
        if type(processed_node) != FunctionCallLeftParenNode:
            assert False, "TODO(map) Raise no left paren exception"
        # Set up the list for holding the print args
        print_arg_node_list = [processed_node]

        # Process the next node
        processed_node = self.process_token()
        while type(processed_node) != FunctionCallRightParenNode:
            # TODO(map) This should really be done in a better way.
            if type(processed_node) == list:
                raise InvalidMacroDeclaration(print_node.token.row, print_node.token.col, PRINT, is_ref=True)
            else:
                print_arg_node_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        print_arg_node_list.append(processed_node)

        line_of_lines = []
        line_of_nodes = []
        for node in print_arg_node_list:
            if type(node) in [ArgSeparatorNode, FunctionCallRightParenNode]:
                line_of_lines.append(line_of_nodes)
                line_of_nodes = []
            elif type(node) == FunctionCallLeftParenNode:
                pass
            else:
                line_of_nodes.append(node)

        print_args = []
        for line_of_nodes in line_of_lines:
            node = self.build_ast_from_node_list(line_of_nodes)
            if node:
                print_args.append(node)

        # Check the arg count is ok
        if len(print_args) < 1:
            raise KeywordMisuseException(print_node.token.row, print_node.token.col, print_node.token.value, PRINT_SIGNATURE)
        if len(print_args) > 1:
            raise TooManyArgsException(print_node.token.row, print_node.token.col)

        # Set the parent node and arg nodes appropriately.
        for node in print_args:
            node.parent_node = print_node
        print_node.arg_nodes = print_args
        
        # Move past the end of line token
        self.process_token()

        return print_node

    def build_update_char_line_ast(self, update_char_node):
        processed_node = self.process_token()
        if type(processed_node) != FunctionCallLeftParenNode:
            raise KeywordMisuseException(update_char_node.token.row, update_char_node.token.col, update_char_node.value, UPDATE_CHAR_SIGNATURE)

        update_char_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            update_char_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        update_char_arg_list.append(processed_node)

        update_char_args = self.build_function_args_ast(update_char_arg_list)

        # Check the arg count is ok
        if len(update_char_args) < 3:
            raise KeywordMisuseException(update_char_node.token.row, update_char_node.token.col, update_char_node.token.value, UPDATE_CHAR_SIGNATURE)
        if len(update_char_args) > 3:
            raise TooManyArgsException(update_char_node.token.row, update_char_node.token.col)

        for node in update_char_args:
            node.parent_node = update_char_node
        update_char_node.arg_nodes = update_char_args

        # Move past the end of line token
        self.process_token()
        
        return update_char_node

    def build_char_at_line_ast(self, char_at_node):
        # Get the left paren node
        processed_node = self.process_token()
        if type(processed_node) != FunctionCallLeftParenNode:
            raise KeywordMisuseException(char_at_node.token.row, char_at_node.token.col, char_at_node.value, CHAR_AT_SIGNATURE)

        char_at_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            char_at_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        char_at_arg_list.append(processed_node)

        line_of_lines = []
        line_of_nodes = []
        for node in char_at_arg_list:
            if type(node) in [ArgSeparatorNode, FunctionCallRightParenNode]:
                line_of_lines.append(line_of_nodes)
                line_of_nodes = []
            elif type(node) == FunctionCallLeftParenNode:
                pass
            else:
                line_of_nodes.append(node)

        char_at_args = []
        for line_of_nodes in line_of_lines:
            node = self.build_ast_from_node_list(line_of_nodes)
            if node:
                char_at_args.append(node)

        # Check the arg count is ok
        if len(char_at_args) < 2:
            raise KeywordMisuseException(char_at_node.token.row, char_at_node.token.col, char_at_node.token.value, CHAR_AT_SIGNATURE)
        if len(char_at_args) > 2:
            raise TooManyArgsException(char_at_node.token.row, char_at_node.token.col)

        # Check that params are the correct type.
        if type(char_at_args[0]) not in [StringNode, VariableReferenceNode]:
            raise InvalidArgsException(char_at_node.token.row, char_at_node.token.col, char_at_node.token.value, type(char_at_args[0]))
        if type(char_at_args[0]) == VariableReferenceNode and self.variable_to_type_map.get(char_at_args[0].value) != STRING:
            raise InvalidArgsException(char_at_node.token.row, char_at_node.token.col, char_at_node.token.value, self.variable_to_type_map.get(char_at_args[0].value))
        if type(char_at_args[1]) not in [NumberNode, VariableReferenceNode, PlusMinusNode]:
            raise InvalidArgsException(char_at_node.token.row, char_at_node.token.col, char_at_node.token.value, type(char_at_args[1]))
        if type(char_at_args[1]) == VariableReferenceNode and self.variable_to_type_map.get(char_at_args[1].value) not in INT_KEYWORDS:
            raise InvalidArgsException(char_at_node.token.row, char_at_node.token.col, char_at_node.token.value, self.variable_to_type_map.get(char_at_args[1].value))

        # Set the parent node and arg nodes appropriately.
        for node in char_at_args:
            node.parent_node = char_at_node
        char_at_node.arg_nodes = char_at_args
        
        # Normally there would be a line to move past the end of line token but
        # in the case where the char at call is made within a variable
        # declaration, such as:
        # char x = charAt("Hello", 0);
        # there is a bug that could arise where a node get processed as a line
        # of work when it shouldn't be.
        # To see this bug, add back:
        # self.process_token()
        # and run the following two lines:
        # charAt("Hello", 0);
        # char x = charAt("Hello", 0);
        
        return char_at_node

    def build_copy_str_line_ast(self, copy_str_node):
        # Get the left paren node
        processed_node = self.process_token()
        if type(processed_node) != FunctionCallLeftParenNode:
            raise KeywordMisuseException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.value, COPY_STR_SIGNATURE)

        copy_str_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            copy_str_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        copy_str_arg_list.append(processed_node)

        copy_str_args = self.build_function_args_ast(copy_str_arg_list)

        # Check the arg count is ok
        if len(copy_str_args) < 2:
            raise KeywordMisuseException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.token.value, COPY_STR_SIGNATURE)
        if len(copy_str_args) > 2:
            raise TooManyArgsException(copy_str_node.token.row, copy_str_node.token.col)

        # Check that params are the correct type.
        if type(copy_str_args[0]) not in [StringNode, VariableReferenceNode]:
            raise InvalidArgsException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.token.value, type(copy_str_args[0]))
        if type(copy_str_args[0]) == VariableReferenceNode and self.variable_to_type_map.get(copy_str_args[0].value) != STRING:
            raise InvalidArgsException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.token.value, self.variable_to_type_map.get(copy_str_args[0].value))
        if type(copy_str_args[1]) not in [StringNode, VariableReferenceNode]:
            raise InvalidArgsException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.token.value, type(copy_str_args[1]))
        if type(copy_str_args[1]) == VariableReferenceNode and self.variable_to_type_map.get(copy_str_args[1].value) != STRING:
            raise InvalidArgsException(copy_str_node.token.row, copy_str_node.token.col, copy_str_node.token.value, self.variable_to_type_map.get(copy_str_args[1].value))

        # Set the parent node and arg nodes appropriately.
        for node in copy_str_args:
            node.parent_node = copy_str_node
        copy_str_node.arg_nodes = copy_str_args

        # Move past the end of line token
        self.process_token()
 
        return copy_str_node

    def build_loop_up_line_ast(self, loop_up_node):
        self.if_else_list.append(loop_up_node)
        # Get the left paren node
        processed_node = self.process_token()

        loop_up_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            loop_up_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        loop_up_arg_list.append(processed_node)
        
        # TODO(map) This is not good but for now it'll raise the correct error
        for node in loop_up_arg_list:
            if type(node) == ArgSeparatorNode:
                raise TooManyArgsException(loop_up_node.token.row, loop_up_node.token.col)

        # Build the list of args
        loop_up_args = self.build_loop_up_down_args(loop_up_arg_list)

        # TODO(map) Also not good but we can have the validation here for now
        if len(loop_up_args) == 0:
            raise KeywordMisuseException(loop_up_node.token.row, loop_up_node.token.col, LOOP_UP, LOOP_UP_SIGNATURE)

        loop_up_arg = loop_up_args[0]
        loop_arg_is_var = type(loop_up_arg) == VariableReferenceNode
        loop_arg_is_number = type(loop_up_arg) == NumberNode
        loop_arg_is_num_var = type(loop_up_arg) == VariableReferenceNode and self.variable_to_type_map.get(loop_up_arg.value) in INT_KEYWORDS
        # Case where arg is not variable but is not correct node type
        if not loop_arg_is_var and not loop_arg_is_number:
            raise InvalidArgsException(loop_up_node.token.row, loop_up_node.token.col, LOOP_UP, type(loop_up_arg))
        # Case of not number node and variable node and variable type not good
        if not loop_arg_is_number and loop_arg_is_var and not loop_arg_is_num_var:
            raise InvalidArgsException(loop_up_node.token.row, loop_up_node.token.col, LOOP_UP, self.variable_to_type_map.get(loop_up_arg.value))

        # Set the parent node and arg nodes appropriately.
        loop_up_node.child_node = loop_up_arg
        loop_up_arg.parent_node = loop_up_node

        # Check we have a left curl brace for distinguishing the loop body of
        # work
        if type(self.process_token()) != LoopBodyLeftCurlNode:
            assert False, "TODO(map) Raise no left curl brace exception"

        body_node_list = []

        # Process next node
        processed_node = self.process_token()
        if type(processed_node) == LoopBodyRightCurlNode:
            assert False, "TODO(map) Raise empty loop body exception"
        while type(processed_node) != LoopBodyRightCurlNode:
            # TODO(map) Should figure out a way to catch going out of the loop
            # The problem is when processing a token, if we don't update the
            # code to ensure that the closing curl brace is also a function body
            # closing brace we will thrown an error that isn't quite correct.
            # This applies to all the loops that are being built up
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
                line_ast = self.build_print_ast(processed_node)
            elif type(processed_node) == FunctionKeywordNode and processed_node.value == COPY_STR:
                line_ast = self.build_copy_str_line_ast(processed_node)
            elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
                line_ast = self.build_var_dec_line_ast(processed_node)
            elif type(processed_node) == LoopUpKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopUpInclusiveKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopDownKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopDownInclusiveKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopFromKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            elif type(processed_node) == LoopFromInclusiveKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
                line_ast = self.build_if_conditional_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == ELSE:
                assert False, "WRITE ME ELSE"
            # We don't want to do anything on a NoOpNode because that means the
            # comment is the only thing on the line.
            elif type(processed_node) == NoOpNode:
                line_ast = processed_node
            else:
                line_ast = self.build_non_keyword_line_ast(processed_node)
                # TODO(map) Be aware of this warning.
                # print("WARNING: There may be a problem in the loop body.")

            if type(processed_node) != NoOpNode:
                body_node_list.append(line_ast)

            # Process the next node
            processed_node = self.process_token()
       
        for node in body_node_list:
            node.parent_node = loop_up_node
        loop_up_node.loop_body = body_node_list

        return loop_up_node

    def build_loop_down_line_ast(self, loop_down_node):
        self.if_else_list.append(loop_down_node)
        # Get the left paren node
        processed_node = self.process_token()

        loop_down_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            loop_down_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        loop_down_arg_list.append(processed_node)

        # TODO(map) This is not good but for now it'll raise the correct error
        for node in loop_down_arg_list:
            if type(node) == ArgSeparatorNode:
                raise TooManyArgsException(loop_down_node.token.row, loop_down_node.token.col)

        # Build the list of args
        loop_down_args  = self.build_loop_up_down_args(loop_down_arg_list)

        # TODO(map) Also not good but we can have the validation here for now
        if len(loop_down_args) == 0:
            raise KeywordMisuseException(loop_down_node.token.row, loop_down_node.token.col, LOOP_DOWN, LOOP_DOWN_SIGNATURE)

        loop_down_arg = loop_down_args[0]
        loop_arg_is_var = type(loop_down_arg) == VariableReferenceNode
        loop_arg_is_number = type(loop_down_arg) == NumberNode
        loop_arg_is_num_var = type(loop_down_arg) == VariableReferenceNode and self.variable_to_type_map.get(loop_down_arg.value) in INT_KEYWORDS
        if not loop_arg_is_var and not loop_arg_is_number:
            raise InvalidArgsException(loop_down_node.token.row, loop_down_node.token.col, LOOP_DOWN, type(loop_down_arg))
        if not loop_arg_is_number and loop_arg_is_var and not loop_arg_is_num_var:
            raise InvalidArgsException(loop_down_node.token.row, loop_down_node.token.col, LOOP_DOWN, self.variable_to_type_map.get(loop_down_arg.value))

        # Set the parent node and arg nodes appropriately.
        loop_down_node.child_node = loop_down_arg
        loop_down_arg.parent_node = loop_down_node

        # Check we have a left curl brace for distinguishing the loop body of
        # work
        if type(self.process_token()) != LoopBodyLeftCurlNode:
            assert False, "TODO(map) Raise no left curl brace exception"

        body_node_list = []

        # Process next node
        processed_node = self.process_token()
        if type(processed_node) == LoopBodyRightCurlNode:
            assert False, "TODO(map) Raise empty loop body exception"
        while type(processed_node) != LoopBodyRightCurlNode:
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
                line_ast = self.build_print_ast(processed_node)
            elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
                line_ast = self.build_var_dec_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
                self.build_if_conditional_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == ELSE:
                assert False, "WRITE ME ELSE"
            elif type(processed_node) == LoopUpKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopUpInclusiveKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopDownKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopDownInclusiveKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopFromKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            elif type(processed_node) == LoopFromInclusiveKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            # We don't want to do anything on a NoOpNode because that means the
            # comment is the only thing on the line.
            elif type(processed_node) == NoOpNode:
                line_ast = processed_node
            else:
                line_ast = self.build_non_keyword_line_ast(processed_node)
                # TODO(map) Be aware of this warning.
                # print("WARNING: There may be a problem in the loop body.")

            if type(processed_node) != NoOpNode:
                body_node_list.append(line_ast)

            # Process the next node
            processed_node = self.process_token()
       
        for node in body_node_list:
            node.parent_node = loop_down_node
        loop_down_node.loop_body = body_node_list

        return loop_down_node

    def build_loop_from_line_ast(self, loop_from_node):
        self.if_else_list.append(loop_from_node)
        # Get the left paren node
        processed_node = self.process_token()

        loop_from_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            loop_from_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        loop_from_arg_list.append(processed_node)

        # Build the list of args
        loop_from_args = self.build_loop_args(loop_from_arg_list)

        # TODO(map) Also not good but we can have the validation here for now
        if len(loop_from_args) == 0:
            raise KeywordMisuseException(loop_from_node.token.row, loop_from_node.token.col, LOOP_FROM, LOOP_FROM_SIGNATURE)

        loop_from_arg = loop_from_args[0]
        # Set the parent node and arg nodes appropriately.
        loop_from_node.child_node = loop_from_arg
        loop_from_arg.parent_node = loop_from_node

        # Check we have a left curl brace for distinguishing the loop body of
        # work
        if type(self.process_token()) != LoopBodyLeftCurlNode:
            assert False, "TODO(map) Raise no left curl brace exception"

        body_node_list = []

        # Process next node
        processed_node = self.process_token()
        if type(processed_node) == LoopBodyRightCurlNode:
            assert False, "TODO(map) Raise empty loop body exception"
        while type(processed_node) != LoopBodyRightCurlNode:
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
                line_ast = self.build_print_ast(processed_node)
            elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
                line_ast = self.build_var_dec_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
                self.build_if_conditional_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == ELSE:
                assert False, "WRITE ME ELSE"
            elif type(processed_node) == LoopUpKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopUpInclusiveKeywordNode:
                line_ast = self.build_loop_up_line_ast(processed_node)
            elif type(processed_node) == LoopDownKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopDownInclusiveKeywordNode:
                line_ast = self.build_loop_down_line_ast(processed_node)
            elif type(processed_node) == LoopFromKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            elif type(processed_node) == LoopFromInclusiveKeywordNode:
                line_ast = self.build_loop_from_line_ast(processed_node)
            # We don't want to do anything on a NoOpNode because that means the
            # comment is the only thing on the line.
            elif type(processed_node) == NoOpNode:
                line_ast = processed_node
            else:
                line_ast = self.build_non_keyword_line_ast(processed_node)
                # TODO(map) Be aware of this warning.
                # print("WARNING: There may be a problem in the loop body.")

            if type(processed_node) != NoOpNode:
                body_node_list.append(line_ast)

            # Process the next node
            processed_node = self.process_token()
       
        for node in body_node_list:
            node.parent_node = loop_from_node
        loop_from_node.loop_body = body_node_list

        return loop_from_node

    def build_return_statement(self, return_node):
        
        # Start by getting first node of the return statement
        processed_node = self.process_token()

        # TODO(map) https://trello.com/c/4RqOmPGH/36-explore-ability-to-return-something-other-than-literals-or-expressions-in-functions
        # Call the build_line_ast method since a return statement does not have
        # the ability to return anything else.
        ret_statement = self.build_non_keyword_line_ast(processed_node)

        return_node.return_body = ret_statement
        ret_statement.parent_node = return_node
        return return_node

    def build_func_reference(self, func_reference_node):
        # Get the left paren node
        processed_node = self.process_token()
        if type(processed_node) != FunctionCallLeftParenNode:
            assert False, "TODO(map) Raise correct func reference exception"

        func_ref_arg_list = []
        while type(processed_node) != FunctionCallRightParenNode:
            func_ref_arg_list.append(processed_node)
            processed_node = self.process_token()

        # Add the closing function call right paren node
        func_ref_arg_list.append(processed_node)

        line_of_lines = []
        line_of_nodes = []
        for node in func_ref_arg_list:
            if type(node) in [ArgSeparatorNode, FunctionCallRightParenNode]:
                line_of_lines.append(line_of_nodes)
                line_of_nodes = []
            elif type(node) == FunctionCallLeftParenNode:
                pass
            else:
                line_of_nodes.append(node)

        func_ref_args = []
        for line_of_nodes in line_of_lines:
            node = self.build_ast_from_node_list(line_of_nodes)
            if node:
                func_ref_args.append(node)

        # TODO(map) Cover type checking of the args passed vs expected types

        # Set the parent node and arg nodes appropriately.
        for node in func_ref_args:
            node.parent_node = func_reference_node
        func_reference_node.function_args = func_ref_args
              
        return func_reference_node

    def build_var_dec_line_ast(self, var_node):
        # Set the flag for if the var is a const
        var_is_const = (type(var_node) == VariableKeywordNode and var_node.value == CONST)

        # The node passed to us was the keyword "const" so we still need to get
        # the type, unlike a variable that can be modified where the node that
        # was passed is the type.
        if var_is_const:
            var_type_node = self.process_token()

        # Get the variable name and the assignment
        var_name_node = self.process_token()
        assignment_node = self.process_token()

        # Handle getting everything to the right of the equal sign
        value_node_list = []
        processed_node = self.process_token()
        while type(processed_node) != EndOfLineNode:

            if type(processed_node) == FunctionKeywordNode and processed_node.value == CHAR_AT:
                char_at_node = self.build_char_at_line_ast(processed_node)
                value_node_list.append(char_at_node)
            elif type(processed_node) == FunctionReferenceNode:
                fn_return_node = self.build_func_reference(processed_node)
                value_node_list.append(fn_return_node)
            else:
                value_node_list.append(processed_node)
            processed_node = self.process_token()

        # TODO(map) This may not always work
        # Set the value_node to the first node.
        value_node = value_node_list[0]

        assigning_fn_return_value = type(value_node) == FunctionReferenceNode
        var_typing = var_type_node.value if var_is_const else var_node.value
        if assigning_fn_return_value :
            if var_typing != self.fn_name_ret_type_map[value_node.value]:
                raise InvalidTypeDeclarationException(var_name_node.token.row, var_name_node.token.col)
        else:
            if var_typing == BOOL and type(value_node) != BooleanNode:
                raise InvalidTypeDeclarationException(var_name_node.token.row, var_name_node.token.col)
            elif var_typing == STRING and type(value_node) != StringNode:
                raise InvalidTypeDeclarationException(var_name_node.token.row, var_name_node.token.col)
            # TODO(map) This probably isn't great as it would pass for any function regardless of its return type
            elif var_typing == CHAR and type(value_node) not in [CharNode, FunctionKeywordNode]:
                raise InvalidTypeDeclarationException(var_name_node.token.row, var_name_node.token.col)
            elif var_typing == INT_64 and type(value_node) != NumberNode:
                raise InvalidTypeDeclarationException(var_name_node.token.row, var_name_node.token.col)
        
        type_to_max_val = {
            INT_8: 255,
            INT_16: 65536,
            INT_32: 4294967296,
            INT_64: 14294967296, # TODO(map) Get the right number
            }
        # TODO(map) Need to make a method to walk the right side and calculate
        # the right side value to raise an error.
        if var_is_const:
            max_value = type_to_max_val.get(var_type_node.value)
        else:
            max_value = type_to_max_val.get(var_node.value)

        if type(value_node) == NumberNode and max_value < int(value_node.value):
            raise BufferOverflowException(var_name_node.token.row, var_name_node.token.col) 

        # TODO(map) This may not always be the correct way of doing things
        if len(value_node_list) > 1:
            value_node = self.build_arithmetic_line_ast(value_node_list)

        # Set up child/parent relationships
        assignment_node.left_side = var_name_node
        var_name_node.parent_node = assignment_node
        assignment_node.right_side = value_node
        value_node.parent_node = assignment_node

        if var_is_const:
            var_type_node.child_node = assignment_node
            assignment_node.parent_node = var_type_node
            var_node.child_node = var_type_node
            var_type_node.parent_node = var_node
        else:
            var_node.child_node = assignment_node
            assignment_node.parent_node = var_node

        if var_is_const:
            self.variable_to_type_map[var_type_node.child_node.left_side.value] = var_type_node.value
        else:
            self.variable_to_type_map[var_node.child_node.left_side.value] = var_node.value

        return var_node

    def build_if_conditional_line_ast(self, if_node):
        self.if_else_list.append(if_node)
        # Check we have a left paren for conditional.
        if type(self.process_token()) != ConditionalLeftParenNode:
            assert False, "TODO(map) Raise improper IF style exception"

        # Set up list of nodes that will be used for the conditional
        conditional_node_list = []
        # Process the next token
        processed_node = self.process_token()
        if type(processed_node) == ConditionalRightParenNode:
            assert False, "TODO(map) Raise empty if conditional exception"
        while type(processed_node) != ConditionalRightParenNode:
            conditional_node_list.append(processed_node)
            processed_node = self.process_token()

        # Build the node that is the actual comparison on the if statement
        conditional_ast = self.build_conditional_line_ast(conditional_node_list)

        # Check we have a left curl brace for distinguishing the conditional
        # body of work if condition is met
        if type(self.process_token()) != IfBodyLeftCurlNode:
            assert False, "TODO(map) Raise no left curl brace exception"

        body_node_list = []

        # Process next node
        processed_node = self.process_token()
        if type(processed_node) == IfBodyRightCurlNode:
            assert False, "TODO(map) Raise empty if body exception"
        while type(processed_node) != IfBodyRightCurlNode:
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
                line_ast = self.build_print_ast(processed_node)
            elif type(processed_node) == FunctionKeywordNode and processed_node.value == UPDATE_CHAR:
                line_ast = self.build_update_char_line_ast(processed_node)
            elif type(processed_node) == FunctionKeywordNode and processed_node.value == COPY_STR:
                line_ast = self.build_copy_str_line_ast(processed_node)
            elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
                line_ast = self.build_var_dec_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
                line_ast = self.build_if_conditional_line_ast(processed_node)
            else:
                line_ast = self.build_non_keyword_line_ast(processed_node)
                # TODO(map) Be aware of this warning.
                # print("WARNING: There may be a problem in the if conditional.")
            body_node_list.append(line_ast)

            # Process the next node
            processed_node = self.process_token()
       
        # Set up child/parent relationships
        if_node.child_node = conditional_ast
        conditional_ast.parent_node = if_node
        for node in body_node_list:
            node.parent_node = if_node
        if_node.true_side = body_node_list

        # We have an else paired with the if and need to add it on to the
        # current if node.
        if self.curr_token.value == ELSE:
            # Process the else token itself
            else_node = self.process_token()
            self.build_else_conditional_line_ast(if_node, else_node)

        return if_node

    def build_else_conditional_line_ast(self, if_node, else_node):
        self.if_else_list.append(else_node)
        
        # Check we have a left curl brace for distinguishing the else body of
        # work.
        if type(self.process_token()) != ElseBodyLeftCurlNode:
            assert False, "TODO(map) Raise no left curl brace exception"

        # Loop until we hit the first real node. This prevents a NoOpNode
        # from being passed in case there are one or more comments before
        # the first line of work in the else.
        processed_node = self.process_token()
        while type(processed_node) == NoOpNode:
            processed_node = self.process_token()

        body_node_list = []

        while type(processed_node) != ElseBodyRightCurlNode:
            if type(processed_node) == FunctionKeywordNode and processed_node.value in [PRINT, PRINTL]:
                line_ast = self.build_print_ast(processed_node)
            elif type(processed_node) == VariableKeywordNode and processed_node.value in VARIABLE_KEYWORDS:
                line_ast = self.build_var_dec_line_ast(processed_node)
            elif type(processed_node) == FunctionKeywordNode and processed_node.value == UPDATE_CHAR:
                line_ast = self.build_update_char_line_ast(processed_node)
            elif type(processed_node) == FunctionKeywordNode and processed_node.value == COPY_STR:
                line_ast = self.build_copy_str_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == IF:
                line_ast = self.build_if_conditional_line_ast(processed_node)
            elif type(processed_node) == LogicKeywordNode and processed_node.value == ELSE:
                assert False, "WRITE ME ELSE"
            else:
                line_ast = self.build_non_keyword_line_ast(processed_node)
                # TODO(map) Be aware of this warning.
                # print("WARNING: There may be a problem in the else conditional.")
            body_node_list.append(line_ast)

            # Process the next node
            processed_node = self.process_token()
       
        # Move past the closing right brace
        self.process_token

        # Set up child/parent relationships
        for node in body_node_list:
            node.parent_node = if_node
        if_node.false_side = body_node_list

        return if_node

    def build_conditional_line_ast(self, line_of_nodes):
        # NOTE: Assumes there are only three nodes, the left side, comparator,
        # and right side for now.
        if len(line_of_nodes) == 3:
            left_side = line_of_nodes[0]
            comparator_node = line_of_nodes[1]
            right_side = line_of_nodes[2]

            # Set up child/parent relationships
            comparator_node.left_side = left_side
            left_side.parent_node = comparator_node
            comparator_node.right_side = right_side
            right_side.parent_node = comparator_node
        else:
            comparator_node = self.build_ast_from_node_list(line_of_nodes)

        return comparator_node

    def build_ast_from_node_list(self, line_of_nodes):
        # NOTE(map) Assumes that everything in the line_of_nodes list is either
        # an expression of some sort (ie comparator, arithmetic, etc) or a
        # literal node (ie strings, numbers, etc). If this is not the case then
        # the logic here falls apart. This is because the nodes in the check
        # below have priorities set correctly so the AST can be built. This also
        # assumes that any node either has no children (primitive node) or only
        # has a left/right side.

        # Check to make sure the nodes are the type expected. This is really
        # bad to have to do because this is called for every list of nodes on
        # a conditional. Should be removed at some point but the assert is nice
        # to have as a safety check
        for node in line_of_nodes:
            assert type(node) in [NumberNode, StringNode, CharNode, BooleanNode, PlusMinusNode, MultiplyDivideNode, CompareNode, VariableReferenceNode, FunctionArgReferenceNode, AssignmentNode, FunctionKeywordNode, LeftParenNode, RightParenNode, FunctionCallLeftParenNode, FunctionCallRightParenNode, ArgSeparatorNode, LoopIdxKeywordNode], f"Type {type(node)} not allowed in AST build."

        # Initialize ast and loop over the list of nodes that should be valid.
        ast = None
        current_working_node = None
        paren_counter = 0
        for node in line_of_nodes:
            # If there is a left paren we add one to the counter so it can be
            # added to the priority of the operation giving it greater or equal
            # priority when needed.
            if type(node) == LeftParenNode:
                paren_counter += 1
            # Subtract away one from the counter if there is a right parent as
            # this means we respect the non-inflated priorities.
            elif type(node) == RightParenNode:
                paren_counter -= 1
            # AST has not been set yet
            elif not ast:
                ast = node
            else:
                # Update the node's priority based on the paren counter
                node.priority += paren_counter

                # There is a node in the tree that is not complete yet.
                if current_working_node:
                    self.check_if_valid_operation(current_working_node.value, current_working_node.left_side, node)
                    if type(node) in [NumberNode, CharNode, StringNode]:
                        current_working_node.right_side = node
                        node.parent_node = current_working_node
                        current_working_node = None
                    else:
                        # Specifically want to error out if we are trying to
                        # set the right side of a node to something other than
                        # a primitive as the current working node should always
                        # be able to handle a child.
                        assert False, "Cannot process current working node."
                # Plus or minus as current op and root of AST is lower or equal prio
                elif type(node) == PlusMinusNode and ast.priority < node.priority:
                    # AST is a primitive so we can just set the side appropriately
                    if type(ast) in [NumberNode, VariableReferenceNode, FunctionArgReferenceNode]:
                        node.left_side = ast
                        ast.parent_node = node
                        ast = node
                    # We need to shuffle some things around
                    else:
                        node.left_side = ast.right_side
                        node.left_side.parent_node = node
                        ast.right_side = node
                        node.parent_node = ast
                        current_working_node = node
                # Plus or minus as current op and root of AST is higher or prio
                elif type(node) == PlusMinusNode and ast.priority >= node.priority:
                    # AST is a compare or assignment node and the right side is set so we have to shuffle nodes
                    if type(ast) in [CompareNode, AssignmentNode]:
                        node.left_side = ast.right_side
                        node.left_side.parent_node = node
                        ast.right_side = node
                        node.parent_node = ast
                        current_working_node = node
                    # Regular case where the left side of the node is assigned the AST
                    else:
                        node.left_side = ast
                        ast.parent_node = node
                        ast = node
                # Multiply or divide as current op and root of AST is lower or equal prio
                elif type(node) == MultiplyDivideNode and ast.priority < node.priority:
                    # AST is a primitive so we can just set the side appropriately
                    if type(ast) == NumberNode:
                        node.left_side = ast
                        ast.parent_node = node
                        ast = node
                    # Otherwise we have to do some shuffling around
                    else:
                        node.left_side = ast.right_side
                        node.left_side.parent_node = node
                        ast.right_side = node
                        node.parent_node = ast
                        current_working_node = node
                # Multiply or divide as current op and root of AST is higher prio
                elif type(node) == MultiplyDivideNode and ast.priority >= node.priority:
                    node.left_side = ast
                    ast.parent_node = node
                    ast = node
                # Assignment as current op
                elif type(node) == AssignmentNode:
                    # Check that AST is a variable reference type
                    if type(ast) != VariableReferenceNode:
                        assert False, "Cannot assign to a non-variable node"
                    node.left_side = ast
                    ast.parent_node = node
                    ast = node
                # Compare is the current op and root of AST is lower prio
                elif type(node) == CompareNode and ast.priority < node.priority:
                    node.left_side = ast
                    ast.parent_node = node
                    ast = node
                # Number or variable reference node used in assignment
                elif type(node) in [NumberNode, VariableReferenceNode] and type(ast) == AssignmentNode:
                    left_side_type = self.variable_to_type_map.get(ast.left_side.value)
                    if type(node) == VariableReferenceNode:
                        right_side_type = self.variable_to_type_map.get(ast.left_side.value)
                    elif type(node) == NumberNode and int(node.value) < 255:
                        right_side_type = INT_8
                    else:
                        assert False, "In assignment and failed to determine type matching."

                    # The left and right sides match so we can just set the ASTs right side
                    if left_side_type == right_side_type:
                        ast.right_side = node
                        node.parent_node = ast
                    # Both the left and right side types are int but they don't match so we have to make sure they fit.
                    elif left_side_type in INT_KEYWORDS and right_side_type in INT_KEYWORDS:
                        if right_side_type == INT_8:
                            int_fits_in_var = True
                        elif right_side_type == INT_16 and left_side_type in [INT_16, INT_32, INT_64]:
                            int_fits_in_var = True
                        elif right_side_type == INT_32 and left_side_type in [INT_32, INT_64]:
                            int_fits_in_var = True
                        elif right_side_type == INT_64 and left_side_type == INT_64:
                            int_fits_in_var = True
                        if int_fits_in_var:
                            ast.right_side = node
                            node.parent_node = ast
                    # The types cannot be paired.
                    else: 
                        raise InvalidAssignmentException(ast.left_side.token.row, ast.left_side.token.col, left_side_type, right_side_type)
                # Variable reference node and root node is compare node
                elif type(node) == VariableReferenceNode and type(ast) == CompareNode:
                    ast.right_side = node
                    node.parent_node = ast
                # Number node and no left side side of the AST
                elif type(node) == NumberNode and not ast.left_side:
                    ast.left_side = node
                    node.parent_node = ast
                # Number node and no right side side of the AST
                elif type(node) == NumberNode and not ast.right_side:
                    ast.right_side = node
                    node.parent_node = ast
                # Char node and no left side side of the AST
                elif type(node) == CharNode and not ast.left_side:
                    ast.left_side = node
                    node.parent_node = ast
                # Char node and no right side side of the AST
                elif type(node) == CharNode and not ast.right_side:
                    ast.right_side = node
                    node.parent_node = ast
                # Boolean node and no left side side of the AST
                elif type(node) == BooleanNode and not ast.left_side:
                    ast.left_side = node
                    node.parent_node = ast
                # Boolean node and no right side side of the AST
                elif type(node) == BooleanNode and not ast.right_side:
                    ast.right_side = node
                    node.parent_node = ast
                # Function node and no left side side of the AST
                elif type(node) == FunctionKeywordNode and not ast.left_side:
                    ast.left_side = node
                    node.parent_node = ast
                # Function node and no right side side of the AST
                elif type(node) == FunctionKeywordNode and not ast.right_side:
                    ast.right_side = node
                    node.parent_node = ast
                # Function arg reference node and no left side side of the AST
                elif type(node) == FunctionArgReferenceNode and not ast.left_side:
                    ast.left_side = node
                    node.parent_node = ast
                # Function arg reference node and no right side side of the AST
                elif type(node) == FunctionArgReferenceNode and not ast.right_side:
                    ast.right_side = node
                    node.parent_node = ast
                else:
                    assert False, f"Not sure how to build AST for {type(node)}"

        return ast

    def build_arithmetic_line_ast(self, line_of_nodes):
        """
        Process a line with an arithmatic unit of work.

        This function is designed around processing any lines of code in the
        language that only contains arithmetic and parenthesis (just PEMDAS ops)
        and shouldn't be used to handle a line of code that contains anything
        else.

        This can be used as a subset of other line ast functions. If a line of
        code were to read:
        `print(3 + 4)`
        this could be called with just the function's parameters as the
        line_of_nodes being passed to the function and return as AST that would
        represent the function args.
        """
        ast = None
        curr_working_node = None
        paren_counter = 0

        for node in line_of_nodes: 
            # If there is a left paren we add one to the counter so it can be
            # added to the priority of the operation giving it greater or equal
            # priority when needed.
            if type(node) == LeftParenNode:
                paren_counter += 1

            # Subtract away one from the counter if there is a right parent as
            # this means we respect the non-inflated priorities.
            elif type(node) == RightParenNode:
                paren_counter -= 1

            # If there is a current working node we need to build off that as
            # opposed to the root node of the AST.
            elif curr_working_node:
                curr_working_node.right_side = node
                node.parent_node = curr_working_node
                # Either the nodes is a basic node and cannot have sides set or
                # the node's left and right sides are populated
                if type(node) != NumberNode and not node.left_side and not node.right_side:
                    curr_working_node = node
                else:
                    curr_working_node = None

            # Not AST set yet and we can set the AST to a node that isn't NoOp
            elif not ast and type(node) not in [LeftParenNode, RightParenNode]:
                ast = node
               
            # The current node has a higher priority than the AST's priority
            # and the current root of the AST is a NumberNode. Only the
            # NumberNode has a priority of LOW
            elif node.priority > ast.priority and ast.priority == LOW:
                node.left_side = ast
                ast.parent_node = node
                ast = node
                # Promote the priority of the AST root node for tracking and
                # comparing later
                ast.priority = ast.priority + paren_counter

            # The current node has a higher priority than the AST's priority
            # and the current root of the AST is some operation. We take the
            # right side of the AST as the left side of the Node and set the
            # right side of the AST to the Node
            elif node.priority + paren_counter > ast.priority:
                node.left_side =  ast.right_side
                ast.right_side.parent_node = node
                ast.right_side = node
                node.parent_node = ast
                # Promote the priority of the AST root node for tracking and
                # comparing later
                ast.priority = ast.priority + paren_counter
                curr_working_node = node
                
            # The current node is lower priority than the root node of the AST
            # and the right side of the AST is not currently set.
            elif node.priority < ast.priority and not ast.right_side:
                ast.right_side = node
                node.parent_node = ast

            # The current node is lower priority than the root node of the AST
            # and the right side has already been set. We need to replace the
            # right side with the current node and if an op, set the
            # curr_working_node
            elif node.priority < ast.priority and ast.right_side:
                node.left_side = ast
                ast.parent_node = node
                ast = node
                curr_working_node = node

            # The priority of the current node and the AST root node are the
            # same and we are not assigning a value so to preserve the tree we
            # will add it to the left side and make a note of where this node
            # lives so we can build off it if needed further on.
            elif node.priority == ast.priority and type(ast) != AssignmentNode:
                node.left_side = ast
                ast.parent_node = node
                ast = node
                curr_working_node = node

            # Opposite of case above where we are assigning a value to some
            # other node (ie updating a var value)
            elif node.priority == ast.priority and type(ast) == AssignmentNode:
                node.right_side = ast
                ast.parent_node = node
                ast = node
                curr_working_node = node

        if type(ast) == AssignmentNode and type(ast.left_side) == VariableReferenceNode:
            if ast.right_side.value.isalpha():
                assignment_type = CHAR
            elif ast.right_side.value.isnumeric():
                if int(ast.right_side.value) < 255:
                    assignment_type = INT_8
            else:
                assert False, "Don't know how to handle assignment value"
        
            assignment_type_matches_var = self.variable_to_type_map.get(ast.left_side.value) == assignment_type
            if not assignment_type_matches_var:
                raise InvalidAssignmentException(ast.left_side.token.row, ast.left_side.token.col, self.variable_to_type_map.get(ast.left_side.value), assignment_type)

        return ast

    def build_function_args_ast(self, line_of_nodes):
        """
        Method for building a list of ASTs that are the function args.

        This requires the outer parenthesis to operate.
        TODO(map) Provide more context here
        """
        # Nothing was passed
        if len(line_of_nodes) == 0:
            return []
        # Only two nodes were passed, check if they are parens meaning empty
        # list
        if len(line_of_nodes) == 2 and type(line_of_nodes[0]) == FunctionCallLeftParenNode and type(line_of_nodes[1]) == FunctionCallRightParenNode:
            return []

        root_node = None
        args_list = []
        for node in line_of_nodes: 
            # Conditional to ensure that we reach a logical end of a function
            # param we add it to the args list.
            type_should_add = type(node) == ArgSeparatorNode or type(node) == FunctionCallRightParenNode
            if root_node and type_should_add:
                args_list.append(root_node)
                root_node = None
            else:
                root_node = node

        return args_list

    def build_loop_up_down_args(self, line_of_nodes):
        # Nothing was passed
        if len(line_of_nodes) == 0:
            return []
        # Only two nodes were passed, check if they are parens meaning empty
        # list
        if len(line_of_nodes) == 2 and type(line_of_nodes[0]) == FunctionCallLeftParenNode and type(line_of_nodes[1]) == FunctionCallRightParenNode:
            return []

        # If the length of the line of nodes is not 3, we could have more or
        # less than the requisite params for the loop. 3 is the current magic
        # number as it includes a left/right paren pair and the single number
        # to loop to
        if len(line_of_nodes) != 3:
            middle_idx = int(len(line_of_nodes) / 2)
            raise InvalidArgsException(line_of_nodes[middle_idx].token.row, line_of_nodes[middle_idx].token.col, "loop", type(line_of_nodes[middle_idx]))

        return [line_of_nodes[1]]

    def build_loop_args(self, line_of_nodes):
        # Nothing was passed
        if len(line_of_nodes) == 0:
            return []
        # Only two nodes were passed, check if they are parens meaning empty
        # list
        if len(line_of_nodes) == 2 and type(line_of_nodes[0]) == FunctionCallLeftParenNode and type(line_of_nodes[1]) == FunctionCallRightParenNode:
            return []

        # If the length of the line of nodes list is not 5, we could have
        # more or less than the requisite params for the loop. 5 is the
        # current magic number as it includes a left/right paren pair, two
        # numbers for the range, and the range node.
        if len(line_of_nodes) != 5:
            middle_idx = int(len(line_of_nodes) / 2)
            raise InvalidArgsException(line_of_nodes[middle_idx].token.row, line_of_nodes[middle_idx].token.col, LOOP_FROM, type(line_of_nodes[middle_idx]))

        range_node = line_of_nodes[2]
        range_node.left_side = line_of_nodes[1]
        line_of_nodes[1].parent_node = range_node 
        range_node.right_side = line_of_nodes[3]
        line_of_nodes[3].parent_node = range_node 

        return [range_node]

    def check_if_valid_operation(self, op_type, left_node, right_node):
        # Checking for add operation being of the same type.
        if op_type == "+":
            if type(left_node) == VariableReferenceNode and self.variable_to_type_map[left_node.value] == STRING and type(right_node) != CharNode:
                raise InvalidConcatenationException(left_node.token.row, left_node.token.col, self.variable_to_type_map[left_node.value], type(right_node))
        # TODO(map) Implement the checks for all the other op types.
        else:
            pass


##########
# Compiler
##########
class Compiler:

    def __init__(self, node_list):
        self.node_list = node_list
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
        self.max_loop_count_depth = 0
        self.curr_loop_count_depth = 0
        self.loop_idx_asm = []
        self.initialize_vars_asm = []
        self.user_func_asm = {}
        self.function_and_args_map = {}
        self.curr_function_name = None

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
        for single_node in self.node_list:
            if type(single_node) == StartNode:
                for node in single_node.children_nodes:
                    asm.extend(self.traverse_tree(node))
                    if self.max_loop_count_depth < self.curr_loop_count_depth:
                        self.max_loop_count_depth = self.curr_loop_count_depth
                    self.curr_loop_count_depth = 0
            elif type(single_node) == FunctionNode:
                self.user_func_asm[single_node.function_name.value] = self.traverse_tree(single_node)
                if self.max_loop_count_depth < self.curr_loop_count_depth:
                    self.max_loop_count_depth = self.curr_loop_count_depth
                self.curr_loop_count_depth = 0
            else:
                asm.extend(self.traverse_tree(single_node))
        return asm

    def write_assembly(self):
        with open(self.output_path, 'a') as compiled_program:
            asm = self.get_assembly()
            # Write any user defined functions in to the assembly file.
            self.write_user_functions()
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
            # TODO(map) Order of operations isn't great here. Should consider
            # making this a method or something
            # Set up the loop index tracking information
            if self.max_loop_count_depth > 0:
                self.loop_idx_asm.append("section .loop_indices write\n")
                for i in range(self.max_loop_count_depth):
                    self.loop_idx_asm.append(f"    loop_idx_{i} dq 0\n")
                    self.loop_idx_asm.append(f"    loop_end_{i} dq 0\n")
            # Write the data for the max depth of the loops. If for instance,
            # there is a max depth of nested loops of three, meaning there is a
            # loop nested in a loop nested in a loop, we will only ever need
            # to track a maximum of three loop indexes at any time.
            for line in self.loop_idx_asm:
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
            if node.value == PRINT:
                if type(node.arg_nodes[0]) == StringNode:
                    keyword_call_asm = self.get_print_string_keyword_asm()
                elif type(node.arg_nodes[0]) == NumberNode:
                    keyword_call_asm = self.get_print_num_keyword_asm()
                elif type(node.arg_nodes[0]) == CharNode:
                    keyword_call_asm = self.get_print_char_keyword_asm()
                elif type(node.arg_nodes[0]) == PlusMinusNode:
                    # TODO(map) https://trello.com/c/wRuStWqL/11-update-the-print-node-logic-for-the-plusminusnode-to-handle-addition-of-things-other-than-strings
                    keyword_call_asm = self.get_print_num_keyword_asm()
                elif self.variables[node.arg_nodes[0].value]:
                    if self.variables[node.arg_nodes[0].value]["var_type"] == "string":
                        keyword_call_asm = self.get_print_string_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "char":
                        keyword_call_asm = self.get_print_char_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "num":
                        keyword_call_asm = self.get_print_num_keyword_asm()
                else:
                    assert False, f"Unsure how to handle the arg {node.arg_nodes[0].value}"
            elif node.value == PRINTL:
                if type(node.arg_nodes[0]) == StringNode:
                    keyword_call_asm = self.get_printl_string_keyword_asm()
                elif type(node.arg_nodes[0]) == NumberNode:
                    keyword_call_asm = self.get_printl_num_keyword_asm()
                elif type(node.arg_nodes[0]) == CharNode:
                    keyword_call_asm = self.get_printl_char_keyword_asm()
                elif type(node.arg_nodes[0]) == PlusMinusNode:
                    # TODO(map) https://trello.com/c/wRuStWqL/11-update-the-print-node-logic-for-the-plusminusnode-to-handle-addition-of-things-other-than-strings
                    keyword_call_asm = self.get_printl_num_keyword_asm()
                elif type(node.arg_nodes[0]) == LoopIdxKeywordNode:
                    keyword_call_asm = self.get_printl_num_keyword_asm()
                elif self.variables[node.arg_nodes[0].value]:
                    if self.variables[node.arg_nodes[0].value]["var_type"] == "string":
                        keyword_call_asm = self.get_printl_string_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "char":
                        keyword_call_asm = self.get_printl_char_keyword_asm()
                    elif self.variables[node.arg_nodes[0].value]["var_type"] == "num":
                        keyword_call_asm = self.get_printl_num_keyword_asm()
            elif node.value == CHAR_AT:
                keyword_call_asm = self.get_char_at_keyword_asm()
            elif node.value == UPDATE_CHAR:
                keyword_call_asm = self.get_update_char_asm()
            elif node.value == COPY_STR:
                # NOTE(map) This will not work with strings with different lengths.
                # Need to implement memory management for this to work.
                keyword_call_asm = self.get_copy_str_asm(self.variables[node.arg_nodes[0].value]["var_len"])
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
                var_val = value_node.value
            elif type(value_node) == CharNode:
                self.char_count += 1
                var_name = f"char_{self.char_count}"
                var_type = "char"
                type_count = self.char_count
                var_val = value_node.value
            elif type(value_node) == NumberNode:
                self.num_count += 1
                var_name = f"number_{self.num_count}"
                var_type = "num"
                type_count = self.num_count
                var_val = value_node.value
            elif type(value_node) == PlusMinusNode:
                # TODO(map) This does not currently support nested values
                self.num_count += 1
                var_name = f"number_{self.num_count}"
                var_type = "num"
                type_count = self.num_count
                if value_node.value == "+":
                    var_val = int(value_node.left_side.value) + int(value_node.right_side.value)
                elif value_node.value == "-":
                    var_val = int(value_node.left_side.value) - int(value_node.right_side.value)
                else:
                    assert False, f"Got a {type(value_node)} with value = {value_node.value}"
            elif type(value_node) == BooleanNode:
                self.bool_count += 1
                var_name = f"bool_{self.bool_count}"
                var_type = BOOL
                type_count = self.bool_count
                var_val = value_node.value
            elif value_node.value == CHAR_AT and type(value_node) == FunctionKeywordNode:
                self.char_count += 1
                var_name = f"char_{self.char_count}"
                type_count = self.char_count
                var_type = "char"
                var_val = value_node.value
                self.initialize_vars_asm.extend(self.traverse_tree(value_node))
                self.initialize_vars_asm.extend(self.get_assign_char_at_value_to_var_asm(var_name))
            elif type(value_node) == FunctionReferenceNode:
                # TODO(map) Need to update the appropriate count based on the type of the function return
                self.num_count += 1
                var_name = f"number_{self.num_count}"
                var_type = "num"
                var_val = value_node.value
                type_count = self.num_count
                self.initialize_vars_asm.extend(self.traverse_tree(value_node))
                # TODO(map) Again, this only works for ints right now
                self.initialize_vars_asm.extend(self.get_assign_new_int_to_var_from_expression(var_name, INT_64))
            else:
                assert False, f"Not sure how to handle Variable of type {type(value_node)} with value {value_node.value}"
            # Check if the variable has the const keyword associated with it.
            if node.is_const:
                asm = self.get_const_creation_asm(self.var_count, type_count, var_val, type(value_node), node.parent_node.parent_node.value)
            else:
                asm = self.get_var_creation_asm(self.var_count, type_count, var_val, type(value_node), node.parent_node.parent_node.value)
            # TODO(map) The `var_len` may not be correct here.
            self.variables[node.value] = {
                "section":  section_text,
                "var_name": var_name,
                "var_type": var_type,
                "var_len": len(value_node.value),
                "var_val": var_val,
                "is_const": True,
                "asm": asm
            }
            # TODO(map) Add the other int types and make this better.
            if node.parent_node.parent_node.value in INT_KEYWORDS:
                self.variables[node.value].update({"int_type": node.parent_node.parent_node.value})

            if not node.is_const:
                if type(value_node) == StringNode:
                    self.initialize_vars_asm.extend(self.get_initialize_var_asm(var_name, len(value_node.value), value_node.value))
                self.variables[node.value]["is_const"] = False
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
            is_const = self.variables[node.value]["is_const"]
            need_str_len = type(node.parent_node) == FunctionKeywordNode and node.parent_node.value in [PRINT, PRINTL]
            if node.can_traverse_to_parent():
                return self.get_push_var_onto_stack_asm(node.value, var_ref, is_const, need_str_len) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_var_onto_stack_asm(node.value, var_ref, is_const, need_str_len)
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
        # TODO(map) Passing the loop values as a tuple isn't great here. I should look for a way to map these to values to I can access them
        # as I desire. This will probably be a problem as things get more complicated, but for now it'll do.
        elif isinstance(node, LoopKeywordNode):
            if type(node) == LoopUpKeywordNode:
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1
                if type(node.child_node) == VariableReferenceNode:
                    asm = self.get_push_loop_up_indices_with_var_asm(node.child_node.value, *self.loops[node]) + self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_asm_end(*self.loops[node])
                else:
                    asm = self.get_push_loop_indices_asm(0, node.child_node.value, *self.loops[node]) + self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_asm_end(*self.loops[node])
                return asm
            elif type(node) == LoopDownKeywordNode:
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1
                if type(node.child_node) == VariableReferenceNode:
                    asm = self.get_push_loop_down_indices_with_var_asm(node.child_node.value, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])
                else:
                    asm = self.get_push_loop_indices_asm(node.child_node.value, 0, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])
                return asm            
            elif type(node) == LoopUpInclusiveKeywordNode:
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1
                if type(node.child_node) == VariableReferenceNode:
                    asm = self.get_push_loop_up_indices_with_var_asm(node.child_node.value, *self.loops[node]) + self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_inclusive_asm_end(*self.loops[node])
                else:
                    asm = self.get_push_loop_indices_asm(0, node.child_node.value, *self.loops[node]) + self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_inclusive_asm_end(*self.loops[node])
                return asm
            elif type(node) == LoopDownKeywordNode:
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1
                if type(node.child_node) == VariableReferenceNode:
                    asm = self.get_push_loop_down_indices_with_var_asm(node.child_node.value, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])
                else:
                    asm = self.get_push_loop_indices_asm(node.child_node.value, 0, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])
                return asm
            elif type(node) == LoopDownInclusiveKeywordNode:
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1
                if type(node.child_node) == VariableReferenceNode:
                    asm = self.get_push_loop_down_indices_with_var_asm(node.child_node.value, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_inclusive_asm_end(*self.loops[node])
                else:
                    asm = self.get_push_loop_indices_asm(node.child_node.value, 0, *self.loops[node]) + self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_inclusive_asm_end(*self.loops[node])
                return asm
            elif type(node) == LoopFromKeywordNode:
                node.visited = True
                # NOTE(map) This assumes that either side of the loopFrom values are a variable or a number.
                first_val_is_var = type(node.child_node.left_side) == VariableReferenceNode
                second_val_is_var = type(node.child_node.right_side) == VariableReferenceNode
                first_loop_value = int(node.child_node.left_side.value) if not first_val_is_var else int(self.variables.get(node.child_node.left_side.value)["var_val"])
                second_loop_value = int(node.child_node.right_side.value) if not second_val_is_var else int(self.variables.get(node.child_node.right_side.value)["var_val"])
                is_loop_ascending = first_loop_value < second_loop_value
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1

                # There are no variable references in the loop from declaration
                if not first_val_is_var and not second_val_is_var:
                    asm = self.get_push_loop_indices_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node]) 
                    if is_loop_ascending:  # Loop up
                        asm += self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_asm_end(*self.loops[node])
                    else:  # Loop down
                        asm += self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])
                # There is a variable reference
                else:
                    # Case of var in first param of loop from
                    if first_val_is_var and not second_val_is_var:
                        asm = self.get_push_loop_from_indices_with_var_first_param_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node])
                    # Case of var in second param of loop from
                    elif not first_val_is_var and second_val_is_var:
                        asm = self.get_push_loop_from_indices_with_var_second_param_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node])
                    # Case of var in first and second param of loop from
                    elif first_val_is_var and second_val_is_var:
                        assert False, "TODO(map) Implement loopFrom with both values being vars"
                    # Catching everything else
                    else:
                        assert False, "There were no var references in loopFrom but logic triggered"

                    if is_loop_ascending:
                        asm += self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_asm_end(*self.loops[node])
                    else:
                        asm += self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_asm_end(*self.loops[node])

                self.curr_loop_count_depth += 1
                self.loop_count += 1
                return asm
            elif type(node) == LoopFromInclusiveKeywordNode:
                node.visited = True
                # NOTE(map) This assumes that either side of the loopFrom values are a variable or a number.
                first_val_is_var = type(node.child_node.left_side) == VariableReferenceNode
                second_val_is_var = type(node.child_node.right_side) == VariableReferenceNode
                first_loop_value = int(node.child_node.left_side.value) if not first_val_is_var else int(self.variables.get(node.child_node.left_side.value)["var_val"])
                second_loop_value = int(node.child_node.right_side.value) if not second_val_is_var else int(self.variables.get(node.child_node.right_side.value)["var_val"])
                is_loop_ascending = first_loop_value < second_loop_value
                node.visited = True
                self.loops[node] = (self.curr_loop_count_depth, self.loop_count)
                self.loop_count += 1
                self.curr_loop_count_depth += 1

                # There are no variable references in the loop from declaration
                if not first_val_is_var and not second_val_is_var:
                    asm = self.get_push_loop_indices_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node]) 
                    if is_loop_ascending:  # Loop up
                        asm += self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_inclusive_asm_end(*self.loops[node])
                    else:  # Loop down
                        asm += self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_inclusive_asm_end(*self.loops[node])
                # There is a variable reference
                else:
                    # Case of var in first param of loop from
                    if first_val_is_var and not second_val_is_var:
                        asm = self.get_push_loop_from_indices_with_var_first_param_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node])
                    # Case of var in second param of loop from
                    elif not first_val_is_var and second_val_is_var:
                        asm = self.get_push_loop_from_indices_with_var_second_param_asm(node.child_node.left_side.value, node.child_node.right_side.value, *self.loops[node])
                    # Case of var in first and second param of loop from
                    elif first_val_is_var and second_val_is_var:
                        assert False, "TODO(map) Implement loopFrom with both values being vars"
                    # Catching everything else
                    else:
                        assert False, "There were no var references in loopFrom but logic triggered"

                    if is_loop_ascending:
                        asm += self.get_loop_up_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_up_inclusive_asm_end(*self.loops[node])
                    else:
                        asm += self.get_loop_down_asm_start(*self.loops[node]) + self.traverse_logic_node_children(node.loop_body) + self.get_loop_down_inclusive_asm_end(*self.loops[node])

                self.curr_loop_count_depth += 1
                self.loop_count += 1
                return asm
            else:
                assert False, f"Not sure how to handle the loop node of type {type(node)}"
        elif type(node) == LoopIdxKeywordNode:
            loop_node = node
            while not isinstance(loop_node, LoopKeywordNode):
                loop_node = loop_node.parent_node
            return self.get_push_current_loop_idx_onto_stack(*self.loops[loop_node])
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
        elif type(node) == MacroNode:
            # Don't need to return assembly here because the Parser already
            # subbed in the relevant nodes where the macro is referenced.
            return []
        elif type(node) == FunctionNode:
            # We need to walk through the function node and set it up as a label
            # that can be referenced and re-used over and over.
            node.visited = True
            return [
                    f"section .text\n",
                    f"    {node.function_name.value}:\n",
                    "        ;; Get return address\n",
                    "        pop rcx\n",
                    "        ;; Get pointer to the args\n",
                    "        pop rdx\n",
                    ] + self.traverse_function_node(node)
        elif type(node) == FunctionReturnNode:
            node.visited = True
            return_body_asm = self.traverse_tree(node.return_body)
            return [
                    "        ;; Push return for this method onto the stack to save a reference\n",
                    "        push rcx\n",
                    ] + return_body_asm + [
                    "        ;; Get return value before pointer reset\n",
                    "        pop rax\n",
                    "        ;; Get return address before pointer reset\n",
                    "        pop rcx\n",
                    "        ;; Reset the pointer to the clean part of the stack\n",
                    "        mov rsp, r8\n",
                    "        ;; Push return value onto stack\n",
                    "        push rax\n",
                    "        ;; Push return address onto stack\n",
                    "        push rcx\n",
                    "        ret\n",
                    ]
        elif type(node) == FunctionReferenceNode:
            func_reference_asm = [
                "    ;; Push pointer to current stack position onto stack\n",
                "    push rsp\n",
            ]
            for idx, arg_node in enumerate(node.function_args):
                func_reference_asm += [f"    ;; Push arg {idx + 1}\n"]
                func_reference_asm += [f"    push {arg_node.value}\n"]
            return func_reference_asm + [
                "    ;; Push pointer to the start of the args\n",
                "    push rsp\n",
                "    ;; Call add function\n",
                f"    call {node.value}\n",
            ]
        elif type(node) == FunctionArgReferenceNode:
            node.visited = True
            arg_loc = self.function_and_args_map[self.curr_function_name][node.value]
            if type(node.parent_node) == AssignmentNode:
                return [] + self.traverse_tree(node.parent_node)
            elif node.can_traverse_to_parent():
                return self.get_push_fn_arg_reference_onto_stack_asm(arg_loc) + self.traverse_tree(node.parent_node)
            else:
                return self.get_push_fn_arg_reference_onto_stack_asm(arg_loc)
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

    def traverse_function_node(self, node):
        # TODO(map) Consider whether or not the language should prevent a user
        # from passing more than some number of functions. This could be
        # beneficial as it would make the ASM easier and potential limit the
        # memory footprint but would also require people to use more complex
        # data structures
        assert len(node.function_args) < 4, "Function arg count greater than 4"

        node.visited = True
        function_body_asm = []

        # Get the of args and pop those into the registers. This will assume
        # for now that the number of args is less than some magical number
        # because it's easier to initially implement but the assertion should
        # go away eventually so you can pass any number of args.
        function_body_asm.extend(["        ;; Get the pointer to the clean stack\n"])
        function_body_asm.extend([f"        mov r8, [rdx + {8 * len(node.function_args)}]\n"])
        reg_num = 9  # Start with r9 for loading args into registers
        arg_to_reg_map = {}
        for idx, arg in enumerate(node.function_args):
            arg_to_reg_map[arg.fn_arg_name.value] = f"r{reg_num}"
            function_body_asm.extend([f"        ;; Get a function argument\n",
                                 f"        mov r{reg_num}, [rdx + {8 * idx}]\n"])
            reg_num += 1

        self.function_and_args_map[node.function_name.value] = arg_to_reg_map
        self.curr_function_name = node.function_name.value

        # TODO(map) This doesn't handle if other data is pushed on the stack
        # before the function args are referenced. If there are a lot of args
        # there's no way to hold them all in the register. Need a way to track
        # the location of the args.
        for body_line in node.function_body:
            function_body_asm += self.traverse_tree(body_line)

        return function_body_asm

    def process_op_node(self, node):
        if node.value == "+":
            # Check if the left side of the add if a variable and its type. If
            # it's a string we don't want to do the basic add assembly.
            if type(node.left_side) == VariableReferenceNode and self.variables[node.left_side.value]["var_type"] == "string":
                return self.get_string_concat_asm(node.left_side.value, self.variables[node.left_side.value]["var_len"])
            else:
                return self.get_add_asm(self.variables.get(node.left_side.value, {}).get("int_type"))
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
                compare_types = CHAR
            else:
                compare_types = INT_64
            return self.get_conditional_equal_asm(self.conditional_count, compare_types)
        elif node.value == "=":
            print_verbose_message(f"Should be assigning for node {node}")
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
                        return self.get_assign_new_int_to_var_from_expression(self.variables[node.left_side.value]["var_name"], self.variables[node.left_side.value]["int_type"])
                elif type(node.right_side) == MultiplyDivideNode:
                    return self.get_assign_new_value_to_var_from_expression(self.variables[node.left_side.value]["var_name"])
                elif node.right_side.value == CHAR_AT:
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
            print_verbose_message(f"Node not doing anything {node}")
            return []
        elif node.value == "..":
            # Don't need to get assembly here because the loop will handle it.
            return []
        else:
            assert False, f"Unrecognized root node value {node.value}"

    def write_user_functions(self):
        with open(self.output_path, 'a') as compiled_program:
            for asm in self.user_func_asm.values():
                for line in asm:
                    compiled_program.write(line)
            
    def create_keyword_functions(self):
        self.create_constant_values()
        self.create_error_string_constants()
        self.create_print_string_function()
        self.create_print_num_function()
        self.create_print_char_function()
        self.create_printl_string_function()
        self.create_printl_num_function()
        self.create_printl_char_function()
        self.create_check_int_8_overflow_function()
        self.create_check_int_16_overflow_function()
        self.create_check_int_32_overflow_function()
        self.create_check_int_64_overflow_function()
        self.create_char_at_function()
        self.create_update_char_function()
        self.create_string_length()
        self.allocate_memory()

    def create_constant_values(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .constants\n")
            compiled_program.write("    divisor dq 10\n")

    def create_error_string_constants(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .error_strings\n")
            compiled_program.write("    int_8_buffer_overflow_string db 'Buffer overflow on int8', 0\n")
            compiled_program.write("    int_16_buffer_overflow_string db 'Buffer overflow on int16', 0\n")
            compiled_program.write("    int_32_buffer_overflow_string db 'Buffer overflow on int32', 0\n")
            compiled_program.write("    int_64_buffer_overflow_string db 'Buffer overflow on int64', 0\n")

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
            compiled_program.write("        ;; Print number function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Set r9 to 0. This will be the bit counter to tell the write\n")
            compiled_program.write("        ;; syscall how many bits to print to the screen.\n")
            compiled_program.write("        mov r9, 0\n")
            compiled_program.write("        ;; Get the value to print into rax\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Put the divisor into the register\n")
            compiled_program.write("        mov r8, [divisor]\n")
            compiled_program.write("        ;; Reset the remainder\n")
            compiled_program.write("        mov rdx, 0\n")
            compiled_program.write("        div r8\n")
            compiled_program.write("        ;; Add 8 bits the counter (r9)\n")
            compiled_program.write("        add r9, 8\n")
            compiled_program.write("        ;; Move rax (quotient) into rbx to reuse\n")
            compiled_program.write("        mov r8, rax\n")
            compiled_program.write("        ;; Push the remainder onto the stack (value to print)\n")
            compiled_program.write("        add rdx, 48\n")
            compiled_program.write("        push rdx\n")
            compiled_program.write("        ;; We need to do an initial check for numbers that are single digit.\n")
            compiled_program.write("        cmp r8, 0\n")
            compiled_program.write("        ;; If single digit number\n")
            compiled_program.write("        je print_print_num\n")
            compiled_program.write("        ;; If not a single digit number\n")
            compiled_program.write("        jne l1_print_num\n")
            compiled_program.write("        l1_print_num:\n")
            compiled_program.write("        mov rax, r8\n")
            compiled_program.write("        ;; Put the divisor into the register\n")
            compiled_program.write("        mov r8, [divisor]\n")
            compiled_program.write("        ;; Reset the remainder\n")
            compiled_program.write("        mov rdx, 0\n")
            compiled_program.write("        div r8\n")
            compiled_program.write("        ;; Move rax (quotient) into rbx to reuse\n")
            compiled_program.write("        mov r8, rax\n")
            compiled_program.write("        ;; Push the remainder onto the stack\n")
            compiled_program.write("        add rdx, 48\n")
            compiled_program.write("        push rdx\n")
            compiled_program.write("        ;; Add 8 bits to the counter (r9)\n")
            compiled_program.write("        add r9, 8\n")
            compiled_program.write("        ;; If remainder then loop again\n")
            compiled_program.write("        cmp r8, 0\n")
            compiled_program.write("        ;; If no numbers remain\n")
            compiled_program.write("        je print_print_num\n")
            compiled_program.write("        ;; If numbers left continue to loop\n")
            compiled_program.write("        jne l1_print_num\n")
            compiled_program.write("        print_print_num:\n")
            compiled_program.write("        ;; Print value\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        mov rdx, r9\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Clean up data on the stack\n")
            compiled_program.write("        clean_print_num_stack:\n")
            compiled_program.write("        ;; Always one value guaranteed or the program wouldn't compile.\n")
            compiled_program.write("        ;; Pop value on stack\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Clobber rax with 8 as we are popping just to clean up stack.\n")
            compiled_program.write("        ;; No sense in using a different reg since we don't care about the value.\n")
            compiled_program.write("        mov rax, 8\n")
            compiled_program.write("        sub r9, rax\n")
            compiled_program.write("        cmp r9, 0\n")
            compiled_program.write("        jne clean_print_num_stack\n")
            compiled_program.write("        je exit_print_num\n")
            compiled_program.write("        exit_print_num:\n")
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
            compiled_program.write("        ;; Print number function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Set r9 to 0. This will be the bit counter to tell the write\n")
            compiled_program.write("        ;; syscall how many bits to print to the screen.\n")
            compiled_program.write("        mov r9, 0\n")
            compiled_program.write("        ;; Get the value to print into rax\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Put the divisor into the register\n")
            compiled_program.write("        mov r8, [divisor]\n")
            compiled_program.write("        ;; Reset the remainder\n")
            compiled_program.write("        mov rdx, 0\n")
            compiled_program.write("        div r8\n")
            compiled_program.write("        ;; Add 8 bits the counter (r9)\n")
            compiled_program.write("        add r9, 8\n")
            compiled_program.write("        ;; Move rax (quotient) into rbx to reuse\n")
            compiled_program.write("        mov r8, rax\n")
            compiled_program.write("        ;; Push the remainder onto the stack (value to print)\n")
            compiled_program.write("        add rdx, 48\n")
            compiled_program.write("        push rdx\n")
            compiled_program.write("        ;; If there is no need to loop go straight to printing\n")
            compiled_program.write("        cmp r8, 0\n")
            compiled_program.write("        ;; If no numbers remain\n")
            compiled_program.write("        je print_printl_num\n")
            compiled_program.write("        l1_printl_num:\n")
            compiled_program.write("        mov rax, r8\n")
            compiled_program.write("        ;; Put the divisor into the register\n")
            compiled_program.write("        mov r8, [divisor]\n")
            compiled_program.write("        ;; Reset the remainder\n")
            compiled_program.write("        mov rdx, 0\n")
            compiled_program.write("        div r8\n")
            compiled_program.write("        ;; Move rax (quotient) into rbx to reuse\n")
            compiled_program.write("        mov r8, rax\n")
            compiled_program.write("        ;; Push the remainder onto the stack\n")
            compiled_program.write("        add rdx, 48\n")
            compiled_program.write("        push rdx\n")
            compiled_program.write("        ;; Add 8 bits to the counter (r9)\n")
            compiled_program.write("        add r9, 8\n")
            compiled_program.write("        ;; If remainder then loop again\n")
            compiled_program.write("        cmp r8, 0\n")
            compiled_program.write("        ;; If no numbers remain\n")
            compiled_program.write("        je print_printl_num\n")
            compiled_program.write("        ;; If numbers left continue to loop\n")
            compiled_program.write("        jne l1_printl_num\n")
            compiled_program.write("        print_printl_num:\n")
            compiled_program.write("        ;; Print value\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        mov rdx, r9\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Clean up data on the stack\n")
            compiled_program.write("        clean_printl_num_stack:\n")
            compiled_program.write("        ;; Always one value guaranteed or the program wouldn't compile.\n")
            compiled_program.write("        ;; Pop value on stack\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Clobber rax with 8 as we are popping just to clean up stack.\n")
            compiled_program.write("        ;; No sense in using a different reg since we don't care about the value.\n")
            compiled_program.write("        mov rax, 8\n")
            compiled_program.write("        sub r9, rax\n")
            compiled_program.write("        cmp r9, 0\n")
            compiled_program.write("        jne clean_printl_num_stack\n")
            compiled_program.write("        je exit_printl_num\n")
            compiled_program.write("        exit_printl_num:\n")
            compiled_program.write("        ;; Add linefeed.\n")
            compiled_program.write("        push 10\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Clean up line feed print\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Add return carriage.\n")
            compiled_program.write("        push 13\n")
            compiled_program.write("        mov rsi, rsp\n")
            compiled_program.write("        mov rdx, 4\n")
            compiled_program.write("        mov rax, 1\n")
            compiled_program.write("        mov rdi, 1\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Clean up line return carriage print\n")
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

    def create_check_int_8_overflow_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("   check_int_8_overflow:\n")
            compiled_program.write("      pop rcx ;; Get return address\n")
            compiled_program.write("      pop rdx ;; Get value to add\n")
            compiled_program.write("      pop rbx ;; Get current value of variable\n")
            compiled_program.write("      movzx rbx, al ;; Move 8 bits into the rax registery\n")
            compiled_program.write("      add al, dl\n")
            compiled_program.write("      jnc no_overflow_int_8\n")
            compiled_program.write("      jc has_overflow_int_8\n")
            compiled_program.write("      no_overflow_int_8:\n")
            compiled_program.write("      push rcx\n")
            compiled_program.write("      ret\n")
            compiled_program.write("      has_overflow_int_8:\n")
            compiled_program.write("      ;; Calculate const string length and push onto stack with string\n")
            compiled_program.write("      push int_8_buffer_overflow_string\n")
            compiled_program.write("      push int_8_buffer_overflow_string\n")
            compiled_program.write("      call string_length\n")
            compiled_program.write("      push int_8_buffer_overflow_string\n")
            compiled_program.write("      ;; Keyword Func\n")
            compiled_program.write("      call print_string\n")
            compiled_program.write("      mov rax, 60\n")
            compiled_program.write("      mov rdi, 8\n")
            compiled_program.write("      syscall\n")

    def create_check_int_16_overflow_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("   check_int_16_overflow:\n")
            compiled_program.write("       pop rcx ;; Get return address\n")
            compiled_program.write("       pop rdx ;; Get value to add\n")
            compiled_program.write("       pop rbx ;; Get current value of variable\n")
            compiled_program.write("       movzx rbx, ax ;; Move 16 bits into the rax registery\n")
            compiled_program.write("       add dx, ax\n")
            compiled_program.write("       jnc no_overflow_int_16\n")
            compiled_program.write("       jc has_overflow_int_16\n")
            compiled_program.write("       no_overflow_int_16:\n")
            compiled_program.write("       push rcx\n")
            compiled_program.write("       ret\n")
            compiled_program.write("       has_overflow_int_16:\n")
            compiled_program.write("       push int_16_buffer_overflow_string\n")
            compiled_program.write("       push int_16_buffer_overflow_string\n")
            compiled_program.write("       call string_length\n")
            compiled_program.write("       push int_16_buffer_overflow_string\n")
            compiled_program.write("       call print_string\n")
            compiled_program.write("       mov rax, 60\n")
            compiled_program.write("       mov rdi, 16 \n")
            compiled_program.write("       syscall\n")

    def create_check_int_32_overflow_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("   check_int_32_overflow:\n")
            compiled_program.write("       pop rcx ;; Get return address\n")
            compiled_program.write("       pop rdx ;; Get value to add\n")
            compiled_program.write("       pop rbx ;; Get current value of variable\n")
            compiled_program.write("       add ebx, edx\n")
            compiled_program.write("       jnc no_overflow_int_32\n")
            compiled_program.write("       jc has_overflow_int_32\n")
            compiled_program.write("       no_overflow_int_32:\n")
            compiled_program.write("       push rcx\n")
            compiled_program.write("       ret\n")
            compiled_program.write("       has_overflow_int_32:\n")
            compiled_program.write("       push int_32_buffer_overflow_string\n")
            compiled_program.write("       push int_32_buffer_overflow_string\n")
            compiled_program.write("       call string_length\n")
            compiled_program.write("       push int_32_buffer_overflow_string\n")
            compiled_program.write("       call print_string\n")
            compiled_program.write("       mov rax, 60\n")
            compiled_program.write("       mov rdi, 32 \n")
            compiled_program.write("       syscall\n")

    def create_check_int_64_overflow_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("   check_int_64_overflow:\n")
            compiled_program.write("       pop rcx ;; Get return address\n")
            compiled_program.write("       pop rdx ;; Get value to add\n")
            compiled_program.write("       pop rbx ;; Get current value of variable\n")
            compiled_program.write("       add rbx, rdx\n")
            compiled_program.write("       jnc no_overflow_int_64\n")
            compiled_program.write("       jc has_overflow_int_64\n")
            compiled_program.write("       no_overflow_int_64:\n")
            compiled_program.write("       push rcx\n")
            compiled_program.write("       ret\n")
            compiled_program.write("       has_overflow_int_64:\n")
            compiled_program.write("       push int_64_buffer_overflow_string\n")
            compiled_program.write("       push int_64_buffer_overflow_string\n")
            compiled_program.write("       call string_length\n")
            compiled_program.write("       push int_64_buffer_overflow_string\n")
            compiled_program.write("       call print_string\n")
            compiled_program.write("       mov rax, 60\n")
            compiled_program.write("       mov rdi, 64 \n")
            compiled_program.write("       syscall\n")

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
            compiled_program.write("        ;; Get byte of string at index\n")
            compiled_program.write("        mov dl, [rax + rbx]\n")
            compiled_program.write("        ;; Push byte back onto stack\n")
            compiled_program.write("        push dx\n")
            compiled_program.write("        ;; Push return address onto stack\n")
            compiled_program.write("        push rcx\n")
            compiled_program.write("        ret\n")

    def create_update_char_function(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    update_char:\n")
            compiled_program.write("        ;; updateChar function\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rcx\n")
            compiled_program.write("        ;; Get the new char\n")
            compiled_program.write("        pop dx\n")
            compiled_program.write("        ;; Get the index to replace\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Load up string\n")
            compiled_program.write("        pop rax\n")
            compiled_program.write("        ;; Move to rdi to replace\n")
            compiled_program.write("        mov rdi, rax\n")
            compiled_program.write("        ;; Update with the char\n")
            compiled_program.write("        mov byte [rdi+rbx], dl\n")
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

    def allocate_memory(self):
        with open(self.output_path, 'a') as compiled_program:
            compiled_program.write("section .text\n")
            compiled_program.write("    allocate_memory:\n")
            compiled_program.write("        ;; Save return address\n")
            compiled_program.write("        pop rbx\n")
            compiled_program.write("        ;; Get current break address\n")
            compiled_program.write("        mov rdi, 0\n")
            compiled_program.write("        mov rax, 12\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Move the current break to rdi\n")
            compiled_program.write("        mov rdi, rax\n")
            compiled_program.write("        ;; Get the number of bytes to allocate\n")
            compiled_program.write("        pop rcx\n")
            compiled_program.write("        ;; Attempt to allocate the bytes\n")
            compiled_program.write("        add rdi, rcx\n")
            compiled_program.write("        mov rax, 12\n")
            compiled_program.write("        syscall\n")
            compiled_program.write("        ;; Set memory address to variable\n")
            compiled_program.write("        pop rcx\n")
            compiled_program.write("        mov qword [rcx], rax\n")
            compiled_program.write("        ;; Push return address onto stack\n")
            compiled_program.write("        push rbx\n")
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

    def get_push_fn_arg_reference_onto_stack_asm(self, arg_loc):
        return [
            "    ;; Push number onto stack\n",
            f"    push {arg_loc}\n"
            ]

    def get_push_var_onto_stack_asm(self, node_value, val, is_const, need_str_len):
        if STRING in val and is_const:
            if need_str_len:
                return [
                    "    ;; Calculate const string length and push onto stack with string\n",
                    f"    push {val}\n",
                    f"    push {val}\n",
                    "    call string_length\n",
                    f"    push {val}\n"
                ]
            else:
                return [
                    "    ;; Push const string onto stack without length\n",
                    f"    push {val}\n"
                ]
        if STRING in val and not is_const:
            if need_str_len:
                return [
                    "    ;; Calculate variable string length and push onto stack with string\n",
                    f"    push qword [{val}]\n",
                    f"    push qword [{val}]\n",
                    "    call string_length\n",
                    f"    push qword [{val}]\n"
                ]
            else:
                return [
                    "    ;; Push variable string onto stack without length\n",
                    f"    push qword [{val}]\n"
                ]
        elif CHAR in val:
            return [
                "    ;; Push char var onto stack\n",
                f"    mov bl, [{val}]\n",
                f"    push bx\n"
            ]
        if self.variables[node_value].get("int_type") == INT_8:
            return [
                "    ;; Push var val onto stack\n",
                f"    mov rax, 0 ;; Clear rax in case it is not empty\n",
                f"    mov al, [{val}]\n",
                f"    movzx rbx, al\n",
                f"    push rbx\n",
            ]
        elif self.variables[node_value].get("int_type") == INT_16:
            return [
                "    ;; Push var val onto stack\n",
                f"    mov rax, 0 ;; Clear rax in case it is not empty\n",
                f"    mov ax, [{val}]\n",
                f"    movzx rbx, ax\n",
                f"    push rbx\n",
            ]
        elif self.variables[node_value].get("int_type") == INT_32:
            return [
                "    ;; Push var val onto stack\n",
                f"    mov rax, 0 ;; Clear rax in case it is not empty\n",
                f"    mov eax, [{val}]\n",
                f"    push rax\n",
            ]
        else:
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

    # TODO(map) Only the left side can be a variable right now. Write a test
    # for the right side that will fail for now.
    def get_add_asm(self, int_type=None):
        asm = ["    ;; Get the two values to add\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Push copy of values to be preserved after overflow check\n",
                "    push rax\n",
                "    push rbx\n",
                "    ;; Push copy of values to be consumed in overflow check\n",
                "    push rax\n",
                "    push rbx\n",
        ]
        if int_type == INT_8:
            asm.append("    call check_int_8_overflow\n")
        elif int_type == INT_16:
            asm.append("    call check_int_16_overflow\n")
        elif int_type == INT_32:
            asm.append("    call check_int_32_overflow\n")
        elif int_type == INT_64 or not int_type:
            asm.append("    call check_int_64_overflow\n")
        return asm + [
                "    ;; Get the values back off the stack\n",
                "    pop rax\n",
                "    pop rbx\n",
                "    ;; Add\n",
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

    def get_update_char_asm(self):
        return [
            "    ;; Keyword Func\n",
            "    call update_char\n"
        ]

    def get_copy_str_asm(self, var_len):
        asm = [
            "    pop rax\n",
            "    pop rbx\n",
        ]
        for i in range(var_len):
            asm.extend([
                f"    mov byte cl, [rbx+{i}]\n",
                f"    mov byte [rax+{i}], cl\n"
            ])
        return asm

    def get_push_loop_start_val_asm(self, loop_start):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    push {loop_start}\n"
        ]

    def get_push_loop_end_val_asm(self, loop_start, loop_end, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    push {loop_end}\n"
        ]

    def get_push_loop_up_indices_with_var_asm(self, var_ref, loop_level, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    mov qword [loop_idx_{loop_level}], 0\n",
            f"    mov rax, [{self.variables[var_ref]['var_name']}]\n",
            f"    mov qword [loop_end_{loop_level}], rax\n",
        ]

    def get_push_loop_down_indices_with_var_asm(self, var_ref, loop_level, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    mov rax, [{self.variables[var_ref]['var_name']}]\n",
            f"    mov qword [loop_idx_{loop_level}], rax\n",
            f"    mov qword [loop_end_{loop_level}], 0\n",
        ]

    def get_push_loop_from_indices_with_var_first_param_asm(self, var_ref, loop_end, loop_level, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    mov rax, [{self.variables[var_ref]['var_name']}]\n",
            f"    mov qword [loop_idx_{loop_level}], rax\n",
            f"    mov qword [loop_end_{loop_level}], {loop_end}\n",
        ]

    def get_push_loop_from_indices_with_var_second_param_asm(self, loop_start, var_ref, loop_level, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    mov qword [loop_idx_{loop_level}], {loop_start}\n",
            f"    mov rax, [{self.variables[var_ref]['var_name']}]\n",
            f"    mov qword [loop_end_{loop_level}], rax\n",
        ]

    def get_push_loop_indices_asm(self, loop_start, loop_end, loop_level, loop_count):
        return [
            "    ;; Push loop start and end on stack\n",
            f"    mov qword [loop_idx_{loop_level}], {loop_start}\n",
            f"    mov qword [loop_end_{loop_level}], {loop_end}\n",
        ]

    def get_loop_up_asm_start(self, loop_level, loop_count):
        return [
            "    ;; Loop up\n",
            f"    loop_{loop_count}:\n",
        ]

    def get_loop_down_asm_start(self, loop_level, loop_count):
        return [
            "    ;; Loop down\n",
            f"    loop_{loop_count}:\n",
        ]

    def get_loop_up_asm_end(self, loop_level, loop_count):
        return [
            "    ;; Compare if counter is below loop end\n",
            f"    mov rcx, [loop_idx_{loop_level}]\n",
            f"    mov rbx, [loop_end_{loop_level}]\n",
            "    inc rcx\n",
            "    cmp rcx, rbx\n",
            f"    mov qword [loop_idx_{loop_level}], rcx\n",
            f"    mov qword [loop_end_{loop_level}], rbx\n",
            f"    jl loop_{loop_count}\n",
        ]

    def get_loop_up_inclusive_asm_end(self, loop_level, loop_count):
        return [
            "    ;; Compare if counter is below loop end\n",
            f"    mov rcx, [loop_idx_{loop_level}]\n",
            f"    mov rbx, [loop_end_{loop_level}]\n",
            "    inc rcx\n",
            "    cmp rcx, rbx\n",
            f"    mov qword [loop_idx_{loop_level}], rcx\n",
            f"    mov qword [loop_end_{loop_level}], rbx\n",
            f"    jle loop_{loop_count}\n",
        ]


    def get_loop_down_asm_end(self, loop_level, loop_count):
        return [
            "    ;; Compare if counter is above loop end\n",
            f"    mov rcx, [loop_idx_{loop_level}]\n",
            f"    mov rbx, [loop_end_{loop_level}]\n",
            "    dec rcx\n",
            "    cmp rcx, rbx\n",
            f"    mov qword [loop_idx_{loop_level}], rcx\n",
            f"    mov qword [loop_end_{loop_level}], rbx\n",
            f"    jg loop_{loop_count}\n",
        ]

    def get_loop_down_inclusive_asm_end(self, loop_level, loop_count):
        return [
            "    ;; Compare if counter is above loop end\n",
            f"    mov rcx, [loop_idx_{loop_level}]\n",
            f"    mov rbx, [loop_end_{loop_level}]\n",
            "    dec rcx\n",
            "    cmp rcx, rbx\n",
            f"    mov qword [loop_idx_{loop_level}], rcx\n",
            f"    mov qword [loop_end_{loop_level}], rbx\n",
            f"    jge loop_{loop_count}\n",
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

    def get_push_current_loop_idx_onto_stack(self, loop_level, loop_count):
        return [
            f"    ;; Push loop idx {loop_level} onto stack\n",
            f"    mov rax, [loop_idx_{loop_level}]\n",
            "    push rax\n",
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
        if compare_types == CHAR:
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

    def get_const_creation_asm(self, var_count, type_count, value, node_type, var_type):
        if node_type == StringNode:
            var_decl = [
                f"    string_{type_count} db '{value}', 0\n",
            ]
        elif node_type == CharNode:
            var_decl = [
                f"    char_{type_count} db '{value}', 0\n",
            ]
        elif node_type == BooleanNode:
            var_decl = [
                f"    bool_{type_count} dq 0\n",
                ] if value == "false" else [
                    f"    bool_{type_count} dq 1\n",
                ]
        elif value == CHAR_AT:
            # Case where we are initializing a variable to the return of a
            # method. We should initialized to 0, then update in the assembly.
            var_decl = [
                f"    char_{type_count} db 0\n",
            ]
        else:
            if var_type == INT_8:
                var_decl = [f"    number_{type_count} db {value}\n"]
            if var_type == INT_16:
                var_decl = [f"    number_{type_count} dw {value}\n"]
            if var_type == INT_32:
                var_decl = [f"    number_{type_count} dd {value}\n"]
            if var_type == INT_64:
                var_decl = [f"    number_{type_count} dq {value}\n"]
        return [
            f"section .var_{var_count}\n",
        ] + var_decl

    def get_var_creation_asm(self, var_count, type_count, value, node_type, var_type):
        if node_type == CharNode:
            var_decl = [
                f"    char_{type_count} db '{value}', 0\n",
            ]
        elif node_type == NumberNode:
            if var_type == INT_8:
                var_decl = [
                    f"    number_{type_count} db {value}\n",
                ]
            if var_type == INT_16:
                var_decl = [
                    f"    number_{type_count} dw {value}\n",
                ]
            if var_type == INT_32:
                var_decl = [
                    f"    number_{type_count} dd {value}\n",
                ]
            if var_type == INT_64:
                var_decl = [
                    f"    number_{type_count} dq {value}\n",
                ]
        elif node_type == PlusMinusNode:
            var_decl = [
                f"    number_{type_count} dq {value}\n",
            ]
        elif node_type == BooleanNode:
            var_decl = [
                f"    bool_{type_count} dq 0\n",
            ] if value == "false" else [
                f"    bool_{type_count} dq 1\n",
            ]
        elif value == CHAR_AT:
            # Case where we are initializing a variable to the return of a
            # method. We should initialized to -1, then update in the assembly.
            var_decl = [
                f"    char_{type_count} db -1\n",
            ]
        elif node_type == FunctionReferenceNode:
            # TODO(map) This only works for int64 right now
            if var_type == INT_64:
                var_decl = [
                        f"    number_{type_count} dq -1\n",
                    ]
            else:
                assert False, f"TODO(map) Implement the type {var_type}"
        elif node_type == StringNode:
            var_decl = [
                f"    string_{type_count} dq 0\n",
            ]
        else:
            assert False, f"Cannot declare var of type {node_type} that is mutable."
        return [
            f"section .var_{var_count} write\n",
        ] + var_decl

    def get_initialize_var_asm(self, var_name, var_len, var_val):
        asm = [
           f"    push {var_name}\n",
           f"    push {var_len+1}\n",
           "    call allocate_memory\n",
           f"    mov rax, qword [{var_name}]\n",
        ]
        for idx, char in enumerate(var_val):
            asm.append(f"    mov byte [rax+{idx}], '{char}'\n")
        asm.append(f"    mov byte [rax+{var_len}], 0\n")
        return asm

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

    def get_assign_new_int_to_var_from_expression(self, var_name, int_type):
        if int_type == INT_8:
            return [
                "    ;; Assign expression value to new var\n",
                "    pop rax\n",
                f"    mov byte [{var_name}], al\n",
            ]
        elif int_type == INT_16:
            return [
                "    ;; Assign expression value to new var\n",
                "    pop rax\n",
                f"    mov word [{var_name}], ax\n",
            ]
        elif int_type == INT_32:
            return [
                "    ;; Assign expression value to new var\n",
                "    pop rax\n",
                f"    mov dword [{var_name}], eax\n",
            ]
        return [
            "    ;; Assign expression value to new var\n",
            "    pop rax\n",
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
    arg_parser.add_argument("--raise-assertions", action="store_true",
                            help="Will raise more verbose messages. For example like the assertions in the __eq__ methods.")
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
    raise_assertion_flag = args.raise_assertions
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
            parser.parse()
            print_verbose_message(parser.get_nodes())
        if args.compile or args.run:
            compiler = Compiler(parser.get_nodes())
            compiler.compile()
        if args.run:
            run_program()
