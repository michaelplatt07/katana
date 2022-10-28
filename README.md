# Katana
## Summary
Katana is a language that was originally developed in Python and compiles straight to assembly. It's designed to be fast and lightweight easy to understand. It takes inspiration in design from C and Python to create an easy to parse syntax for the reader.

## Features
1. Direct compiling to assembly for optimal speed
2. Easy to read syntax
3. Compile time feedback

## Coding in Katana
---
## Basic Arithmetic
Katana supports all the usual mathematic operations.

### Simple Addition
Input
```
1 + 2 + 3
```
Returns
```
6
```

### Simple Subtraction
Input
```
4 - 1 - 1
```
Returns
```
2
```

### Simple Multiplication
Input
```
4 * 2
```
Returns
```
8
```

### Simple Division
Input
```
8 / 8
```
Returns
```
1
```

### Advance Arithmetic
Katana respects order of operations for arithmetic
```
8 / 8 + 3 * 2
```
Returns
```
7
```

## TODO: Features to Implement
[x] Implement subtract in asssembly
[x] Implement multiply in asssembly
[x] Implement divide in asssembly
[ ] Handle parenthesis moving order of operations
[ ] Raise exception in a better way in generate_token
[ ] Store values as variables in assembly
[ ] Enable printing for numbers
[ ] Add additional mathematics like double and float math
[ ] Implement strong typing
[ ] Add functions
[ ] Modulo calcuations
[ ] Formatting numbers like 1_000_000 is supported for easier reading
