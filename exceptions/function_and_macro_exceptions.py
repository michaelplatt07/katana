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
