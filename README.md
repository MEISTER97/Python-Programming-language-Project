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
