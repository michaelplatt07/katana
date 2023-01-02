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

## Coding in Katana
---
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

### Advance Arithmetic
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

## TODO: Features to Implement
- [x] Implement subtract in asssembly
- [x] Implement multiply in asssembly
- [x] Implement divide in asssembly
- [x] Handle parenthesis moving order of operations
- [x] Handle semicolon token to end a line
- [x] Set up printing in assembly
- [ ] Handle string literals
- [ ] Change the program parsing to read line by line
- [ ] Do type parsing in declaration, things like uint32 and such
- [ ] Enable printing for numbers
- [ ] Store values as variables in assembly
- [ ] Add additional mathematics like double and float math
- [ ] Implement strong typing
- [ ] Add functions
- [ ] Modulo calcuations
- [ ] Formatting numbers like 1_000_000 is supported for easier reading
