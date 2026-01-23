##################
# Lexer Exceptions
##################
# TODO(map) Maybe we don't need this one
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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.character == other.character
        )


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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.keyword == other.keyword
        )


class InvalidVariableNameError(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid variable name")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return (
            f"Variable name at {self.line_num}:{self.col_num} cannot start with digit."
        )

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


##################
# Method Exception
##################
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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.keyword == other.keyword
            and self.usage == other.usage
        )


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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.keyword == other.keyword
            and self.arg_type == other.arg_type
        )


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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.string == other.string
        )


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
        return (
            f"else at {self.line_num}:{self.col_num} does not have a matching if block."
        )

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return self.line_num == other.line_num and self.col_num == other.col_num


class InvalidTypeDeclarationException(Exception):
    def __init__(self, line_num, col_num, expected_type, actual_type):
        super().__init__("Invalid type")
        self.line_num = line_num + 1
        self.col_num = col_num
        self.expected_type = expected_type
        self.actual_type = actual_type

    def __str__(self):
        return f"Invalid type at {self.line_num}:{self.col_num}. Expected {self.expected_type} but got {self.actual_type}."

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
        assert (
            self.assignment_type == other.assignment_type
        ), f"{self.assignment_type, other.assignment_type}"
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.base_type == other.base_type
            and self.assignment_type == other.assignment_type
        )


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
        assert (
            self.concat_type == other.concat_type
        ), f"{self.concat_type, other.concat_type}"
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and self.base_type == other.base_type
            and self.concat_type == other.concat_type
        )


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
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and type(self) == type(other)
        )


class InvalidFunctionDeclarationException(Exception):
    def __init__(self, line_num, col_num):
        super().__init__("Invalid Function")
        self.line_num = line_num + 1
        self.col_num = col_num

    def __str__(self):
        return (
            f"{self.line_num}:{self.col_num} Function was declared with invalid syntax."
        )

    def __eq__(self, other):
        assert self.line_num == other.line_num, f"{self.line_num, other.line_num}"
        assert self.col_num == other.col_num, f"{self.col_num, other.col_num}"
        return (
            self.line_num == other.line_num
            and self.col_num == other.col_num
            and type(self) == type(other)
        )


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
