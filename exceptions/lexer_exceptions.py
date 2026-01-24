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
