################
# Var exceptions
################
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
