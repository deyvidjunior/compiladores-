```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, List

# Token types
class TokenType(Enum):
    PROGRAM = auto()
    VAR = auto()
    INTEGER = auto()
    BEGIN = auto()
    END = auto()
    READ = auto()
    WRITE = auto()
    WHILE = auto()
    DO = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LESS_EQUAL = auto()
    OPEN_PAR = auto()
    CLOSE_PAR = auto()
    DOT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

@dataclass
class Symbol:
    identifier: str
    address: int
    type: str

class Compiler:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.current = 0
        self.line = 1
        self.column = 1
        self.symbol_table: List[Symbol] = []
        self.next_address = 0
        self.label_counter = 0

    def next_label(self) -> int:
        self.label_counter += 1
        return self.label_counter

    def add_symbol(self, identifier: str, type_: str) -> None:
        # Check if symbol already exists
        if any(s.identifier == identifier for s in self.symbol_table):
            self.error(f"Semantic error: Variable '{identifier}' already declared")
        
        symbol = Symbol(identifier, self.next_address, type_)
        self.symbol_table.append(symbol)
        self.next_address += 1

    def get_symbol(self, identifier: str) -> Symbol:
        for symbol in self.symbol_table:
            if symbol.identifier == identifier:
                return symbol
        self.error(f"Semantic error: Variable '{identifier}' not declared")

    def error(self, message: str) -> None:
        raise Exception(f"Line {self.line}, Column {self.column}: {message}")

    def compile(self) -> None:
        self.tokenize()
        self.program()

    def program(self) -> None:
        # program identifier;
        self.match(TokenType.PROGRAM)
        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.SEMICOLON)
        
        print("INPP")
        
        # Variable declarations
        self.variable_declarations()
        
        # Begin
        self.match(TokenType.BEGIN)
        
        # Commands
        self.commands()
        
        # End
        self.match(TokenType.END)
        self.match(TokenType.DOT)
        
        print("PARA")

    def variable_declarations(self) -> None:
        if self.current_token().type == TokenType.VAR:
            self.match(TokenType.VAR)
            
            # Process variable declarations
            while True:
                identifiers = self.identifier_list()
                self.match(TokenType.COLON)
                type_ = self.type_()
                self.match(TokenType.SEMICOLON)
                
                # Add variables to symbol table
                for identifier in identifiers:
                    self.add_symbol(identifier, type_)
                
                if self.current_token().type != TokenType.IDENTIFIER:
                    break
            
            # Generate code to allocate memory for variables
            print(f"AMEM {len(self.symbol_table)}")

    def commands(self) -> None:
        self.command()
        while self.current_token().type == TokenType.SEMICOLON:
            self.match(TokenType.SEMICOLON)
            self.command()

    def command(self) -> None:
        if self.current_token().type == TokenType.IDENTIFIER:
            # Assignment
            identifier = self.current_token().lexeme
            symbol = self.get_symbol(identifier)
            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.ASSIGN)
            self.expression()
            print(f"ARMZ {symbol.address}")
            
        elif self.current_token().type == TokenType.WHILE:
            # While loop
            label_start = self.next_label()
            label_end = self.next_label()
            
            print(f"L{label_start}: NADA")
            self.match(TokenType.WHILE)
            self.expression()
            print(f"DSVF L{label_end}")
            self.match(TokenType.DO)
            self.command()
            print(f"DSVS L{label_start}")
            print(f"L{label_end}: NADA")
            
        elif self.current_token().type == TokenType.READ:
            # Read command
            self.match(TokenType.READ)
            self.match(TokenType.OPEN_PAR)
            identifier = self.current_token().lexeme
            symbol = self.get_symbol(identifier)
            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.CLOSE_PAR)
            print("LEIT")
            print(f"ARMZ {symbol.address}")
            
        elif self.current_token().type == TokenType.WRITE:
            # Write command
            self.match(TokenType.WRITE)
            self.match(TokenType.OPEN_PAR)
            self.expression()
            self.match(TokenType.CLOSE_PAR)
            print("IMPR")

    def expression(self) -> None:
        self.term()
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token().type
            self.match(operator)
            self.term()
            if operator == TokenType.PLUS:
                print("SOMA")
            else:
                print("SUBT")

    def term(self) -> None:
        self.factor()
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            operator = self.current_token().type
            self.match(operator)
            self.factor()
            if operator == TokenType.MULTIPLY:
                print("MULT")
            else:
                print("DIVI")

    def factor(self) -> None:
        if self.current_token().type == TokenType.IDENTIFIER:
            symbol = self.get_symbol(self.current_token().lexeme)
            print(f"CRVL {symbol.address}")
            self.match(TokenType.IDENTIFIER)
        elif self.current_token().type == TokenType.NUMBER:
            print(f"CRCT {self.current_token().lexeme}")
            self.match(TokenType.NUMBER)
        else:
            self.match(TokenType.OPEN_PAR)
            self.expression()
            self.match(TokenType.CLOSE_PAR)

    # Helper methods for lexical analysis and token matching
    def tokenize(self) -> None:
        # Implementation of lexical analysis goes here
        pass

    def match(self, expected_type: TokenType) -> None:
        if self.current_token().type == expected_type:
            self.current += 1
        else:
            self.error(f"Expected {expected_type}, got {self.current_token().type}")

    def current_token(self) -> Token:
        if self.current >= len(self.tokens):
            return Token(TokenType.EOF, "", self.line, self.column)
        return self.tokens[self.current]

    def identifier_list(self) -> List[str]:
        identifiers = [self.current_token().lexeme]
        self.match(TokenType.IDENTIFIER)
        
        while self.current_token().type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            identifiers.append(self.current_token().lexeme)
            self.match(TokenType.IDENTIFIER)
            
        return identifiers

    def type_(self) -> str:
        if self.current_token().type == TokenType.INTEGER:
            self.match(TokenType.INTEGER)
            return "integer"
        self.error("Expected type declaration")
```