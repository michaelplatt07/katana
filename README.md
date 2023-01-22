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

### Coverage
Katana uses `coverage` to determine which lines of code are not being tested. Specifically running `coverage run -m pytest tests` will create a coverage folder folder, then run `coverage html` to get a nice output view.

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

## Keywords
### print
Katana supports printing both numbers and strings
```
print(3); // prints the number 3
```
Katana will print mathematic expressions as well
```
print(3+4); // prints the number 7
print(3*2); // prints the number 6
print(3-1); // prints the number 2
```
Hello, World example in Katana
```
print("Hello, World!")
```

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

## TODO: Features to Implement
- [x] Implement subtract in asssembly
- [x] Implement multiply in asssembly
- [x] Implement divide in asssembly
- [x] Handle parenthesis moving order of operations
- [x] Handle semicolon token to end a line
- [x] Set up printing in assembly
- [x] Handle string literals
- [x] Change the program parsing to read line by line
- [ ] Implement a printl for print line that adds new line on to end
- [x] Add conditionals
- [ ] Add to current conditionals (only support `>` right now)
- [ ] Add loops
- [ ] * loopUntil(==, >, <)
- [ ] * loopDown
- [ ] * loopDownIncl
- [ ] * loopUp
- [ ] * loopUpIncl
- [ ] * loopFrom
- [ ] * loopFromIncl
- [ ] * loopOver
- [ ] Add ability to update variable in the code
- [ ] Add 32-bit processing flag
- [ ] Do type parsing in declaration, things like uint32 and such
- [ ] Enable printing for numbers
- [ ] Store values as variables in assembly
- [ ] Add additional mathematics like double and float math
- [ ] Implement strong typing
- [ ] Add functions
- [ ] Modulo calcuations
- [ ] Formatting numbers like 1_000_000 is supported for easier reading
