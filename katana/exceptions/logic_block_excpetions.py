########################
# Logic block exceptions
########################
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
