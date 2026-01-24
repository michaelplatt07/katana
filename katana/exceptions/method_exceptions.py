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
