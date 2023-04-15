# Katana
## Summary
Katana is a language that was originally developed in Python and compiles straight to assembly. It's designed to be fast and lightweight easy to understand. It takes inspiration in design from C and Python to create an easy to parse syntax for the reader.

## Features
1. Direct compiling to assembly for optimal speed
2. Easy to read syntax
3. Compile time feedback

## Testing
### Unit Tests
Running `pytest tests/` will run the full suite of tests. To get a more verbose output you can run `pytest -vv tests/` to see a detailed output.

### Integration tests
There are a number of integration tests to make sure the code works as expected. By runing `python tests/test_programs.py` the integrations tests will be launched. Developers can also use `--display-compare` to see how the data looks and `--create-expected` to recreate the expected output results file. Note that this is very basic functionality and assumes that the results in the expected outputs is correct every time. This should, as it's currently implemented, only be used for regression tests.

### Coverage
Katana uses `coverage` to determine which lines of code are not being tested. Specifically running `coverage run -m pytest tests` will create a coverage folder folder, then run `coverage html` to get a nice output view.

## Vim Highlighting
Copy the folders in the `vim` directory in the project to your local `.vim` config for easy syntax highlighting and code folding.

## Code Structure
### Basic layout
Katana has a single point of entry, the `main` method. Without it, the program is unsure about where to start to build the AST. 

## Code API
---
## Obligatory Hello Program
As with most languages, here's how one would write the hello world program:
```
main() {
    print("Hello, Katana!");
}
```

## Keywords and Types
Katana is a strongly typed language where all variables must be declared with a type for it to be used. An example of declaring a variable would look like:
```
const string x = "Hello, Katana!";
```
Note that in the example above the keyword `const` is prepended to the variable declaration. This implies that the string `x` cannot be modified anywhere in the code. If you wanted to use a string that could be modified you would exclude the const like so:
```
string x = "Hello, Katana!";
```
Below is an exhaustive list of the types in Katana:
* int_16
* string
* bool
* char

## Basic Arithmetic
Katana supports all the usual mathematic operations.

### Simple Addition
Input
```
1 + 2 + 3;
```
Returns
```
6
```

### Simple Subtraction
Input
```
4 - 1 - 1;
```
Returns
```
2
```

### Simple Multiplication
Input
```
4 * 2;
```
Returns
```
8
```

### Simple Division
Input
```
8 / 8;
```
Returns
```
1
```

### Advanced Arithmetic
Katana respects order of operations for arithmetic
```
4 / 1 + 3 * 2;
```
Returns
```
10
```

Using parenthesis changes the outcome of the arithmetic
```
4 / (1 + 3) * 2;
```
Returns
```
2
```

## Builtin Functions
Katana has built in methods that can be used. The exhaustive list can be found here: TODO(map) PROVIDE LINK

### print
Katana supports typical printing capabilities:
```
print(3); // prints the number 3
```
Katana will print mathematic expressions as well
```
print(3+4); // prints the number 7
print(3*2); // prints the number 6
print(3-1); // prints the number 2
```
Printing a char:
```
print('A'); // prints the character A
```
Hello, World example in Katana
```
print("Hello, World!")
```

### charAt
Katana can access characters of a string by index:
```
char x = charAt("Hello, Katana!", 3); // x will be 'l'
```

### copyStr
Katana provides a method to copy the contents of one string to another. Simply doing the following:
```
string x = "Hello";
string y = "olleH";
x = y;
```
will result in the pointer to the string `x` being updated to the pointer for string `y`. Instead, use `copyStr` to copy the contents of a string like so:
```
string x = "Hello";
string y = "olleH";
copyStr(y, x);
```
This will copy the individual bytes while still maintaining the pointer to `y` and `x` separately.

## Keywords
### if/else
Katana supports conditionals with the following format:
```
if (SOME_CONDITION) {
    // do body
} else {
    // do other body
}
```
with `SOME_CONDITION` being a truthy statement like `1 > 0`.

### loops
Katana has basic support for loops but often times in software there is a need to perform basic loop operations such as loop from zero to the size of a list. For that, Katana offers some specialized loops out of the box.

Basic loops use the keyword `loopFrom` like so:
```
main() {
    loopFrom(0..3) { // Loops from 0 - 3, non-inclusive
        // BODY
    }
}
```
`loopUp` is a specialized loop that, by default, starts at `0` and ends at the value in loop definition:
```
main() {
    loopUp(5) { // Loops from 0 - 5, non-inclusive
        // BODY
    }
}
```

`loopDown` is a specialized loop that, by default, starts at the value in the loop definition and loops to `0`:
```
main() {
    loopDown(5) { // Loops from 5 - 0, non-inclusive
        // BODY
    }
}
```


## TODO: Features to Implement
- [x] Implement subtract in asssembly
- [x] Implement multiply in asssembly
- [x] Implement divide in asssembly
- [x] Handle parenthesis moving order of operations
- [x] Handle semicolon token to end a line
- [x] Set up printing in assembly
- [x] Handle string literals
- [x] Change the program parsing to read line by line
- [x] Rule 110
- [x] * Conditional `==`
- [x] * String variables
- [x] * Boolean constants
- [x] * Assignment operator like `x = y + 1`. Currently makes `((x=y)+1)`
- [x] * Substring access? Maybe the char should just exist instead?
- [x] * Conditionals with expressions on both sides like `if (x - 1 > 0)`
- [ ] Update strings
- [x] Implement a printl for print line that adds new line on to end
- [x] Add conditionals
- [ ] Chaining conditionals using `and` and `or` keywords
- [x] Add to current conditionals (only support `>` right now)
- [ ] Add loops
- [ ] * loopUntil(==, >, <)
- [x] * loopDown
- [ ] * loopDownIncl
- [x] * loopUp
- [ ] * loopUpIncl
- [x] * loopFrom
- [ ] * loopFromIncl
- [ ] * loopOver
- [ ] Loop enhancements by accessing the index of the loop
- [ ] Add ability to update variable in the code
- [x] * Update integers
- [ ] Update README with the different types that exist
- [ ] Add 32-bit processing flag
- [ ] Do type parsing in declaration, things like uint32 and such
- [ ] Enable printing for numbers
- [ ] Store values as variables in assembly
- [ ] Add additional mathematics like double and float math
- [ ] Implement strong typing
- [ ] Add functions
- [ ] Modulo calcuations
- [ ] Formatting numbers like 1_000_000 is supported for easier reading
- [ ] Add ability to exclude code during compilation. This is similar to #define
- [ ] Update anywhere the pointers are being used to use `LEA` instead of `MOV`
