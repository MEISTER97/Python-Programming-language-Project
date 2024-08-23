# Part A
# Custom Interpreter

## Overview

This project features a custom interpreter for a domain-specific language (DSL) that allows for basic arithmetic operations, boolean logic, function definitions, and lambda expressions. This interpreter is built in Python and is an educational tool for understanding the fundamentals of interpreters and language parsing.

## Components

### Lexer

The **Lexer** tokenizes the input source code into discrete symbols (tokens). It recognizes:
- Arithmetic operators (`+`, `-`, `*`, `/`, `%`, `^`)
- Comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
- Logical operators (`&&`, `||`, `!`)
- Delimiters (`(`, `)`, `,`, `->`, `.`)
- Keywords (`FUNC`, `LAMBDA`, `IF`, `THEN`, `ELIF`, `ELSE`)
- Identifiers and literals (integers, floats)

### Parser

The **Parser** converts tokens into an abstract syntax tree (AST). It supports:
- Arithmetic expressions
- Boolean expressions
- Function and lambda definitions
- Conditional statements (`IF`, `THEN`, `ELIF`, `ELSE`)

### Evaluator

The **Evaluator** executes the AST. It handles:
- Performing arithmetic and boolean operations
- Calling functions and evaluating lambda expressions
- Managing variable scopes and function recursion

## How It Works

1. **Input Processing**: The input source code is read and processed by the Lexer, which breaks it into tokens.
2. **Parsing**: The Parser takes the tokens and constructs an AST that represents the hierarchical structure of the code.
3. **Evaluation**: The Evaluator traverses the AST and performs the specified computations or operations to produce a result.


The interpreter is designed to evaluate expressions and execute commands in a custom language that supports arithmetic operations, boolean logic, function definitions, and lambda calculus. It can operate in two modes:

1. **Interactive Mode**: For real-time expression evaluation.
2. **Batch Mode**: For executing a series of commands from a file.

### Running in Interactive Mode
1. Start the Interpreter: Run the script using Python:
   python MainRPEL.py
2. Enter Commands:
   You will be prompted to enter RPEL expressions or commands.
   Type your expression or command and press Enter.
3. Exit:
Type exit or quit to terminate the interactive session.

### Running in Batch Mode
   **Prepare the Script File**:
   - Create a text file named `commands.txt` with each line containing an RPEL expression or command.
   - Run the script with the command file as an argument: python MainRPEL.py commands.txt

## Supported Features
- Arithmetic Operations: Addition, subtraction, multiplication, division.
- Boolean Logic: Logical operators && (AND), || (OR), != (not equal).
- Function Definitions: Define and call functions with support for recursion.
- Lambda Expressions: Single and multi-argument lambda functions.

## Limitations
- Error Handling: The interpreter may not handle all syntax errors gracefully.
- Performance: Complex expressions or large-scale function evaluations may affect performance.

