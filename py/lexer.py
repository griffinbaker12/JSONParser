import argparse
from enum import Enum, auto

from common import print_sandwich, read_file

ESC_CHARS = [
    '"',
    "\\",
    "/",
    "b",
    "f",
    "n",
    "r",
    "t",
]
MIN_ALLOWED_UNICODE, MAX_ALLOWED_UNICODE = 0x20, 0x10FFFF


class TokenType(Enum):
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    COLON = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"


class JSONLexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char in " \t\r":
                self.advance()
            elif char == "\n":
                self.advance(is_new_line=True)
            elif char == "{":
                tokens.append(self.create_token(TokenType.LEFT_BRACE, "{"))
                self.advance()
            elif char == "}":
                tokens.append(self.create_token(TokenType.RIGHT_BRACE, "}"))
                self.advance()
            elif char == "[":
                tokens.append(self.create_token(TokenType.LEFT_BRACKET, "["))
                self.advance()
            elif char == "]":
                tokens.append(self.create_token(TokenType.RIGHT_BRACKET, "]"))
                self.advance()
            elif char == ",":
                tokens.append(self.create_token(TokenType.COMMA, ","))
                self.advance()
            elif char == ":":
                tokens.append(self.create_token(TokenType.COLON, ":"))
                self.advance()
            elif char == '"':
                tokens.append(self.tokenize_string())
            elif char.isdigit() or char == "-":
                tokens.append(self.tokenize_number())
            elif char.isalpha():
                tokens.append(self.tokenize_keyword())
            else:
                raise ValueError(
                    f"Unexpected character: {char} at line {self.line}, column {self.column}"
                )
        return tokens

    def create_token(self, type, value):
        return Token(type, value, self.line, self.column)

    def advance(self, is_new_line=False):
        self.pos += 1
        if is_new_line:
            self.line += 1
            self.column = 1
        else:
            self.column += 1

    def tokenize_string(self):
        start_line, start_column = self.line, self.column
        value = self.text[self.pos]  # Include the opening quote
        self.advance()  # move past initial quote
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char == '"':
                value += char  # Include the closing quote
                self.advance()
                return self.create_token(TokenType.STRING, value)
            elif char == "\\":
                value += char
                self.advance()
                if self.pos >= len(self.text):
                    raise ValueError(
                        f"Unterminated string at line {start_line}, column {start_column}"
                    )
                escape_char = self.text[self.pos]
                if escape_char in ESC_CHARS:
                    value += escape_char
                    self.advance()
                elif escape_char == "u":
                    value += escape_char
                    self.advance()
                    for _ in range(4):
                        if self.pos >= len(self.text):
                            raise ValueError(
                                f"Incomplete Unicode escape sequence at line {self.line}, column {self.column}"
                            )
                        hex_char = self.text[self.pos]
                        if hex_char not in "0123456789ABCDEFabcdef":
                            raise ValueError(
                                f"Invalid Unicode escape sequence at line {self.line}, column {self.column}"
                            )
                        value += hex_char
                        self.advance()
                else:
                    raise ValueError(
                        f"Invalid escape sequence '\\{escape_char}' at line {self.line}, column {self.column}"
                    )
            elif not MIN_ALLOWED_UNICODE <= ord(char) <= MAX_ALLOWED_UNICODE:
                raise ValueError(
                    f"Unescaped control character {repr(char)} at line {self.line}, column {self.column}"
                )
            else:
                value += char
                self.advance()
        raise ValueError(
            f"Unterminated string at line {start_line}, column {start_column}"
        )

    def tokenize_number(self):
        # a number is made up of an integer, fraction, exponent
        # so lets check for all these parts
        start_line, start_column = self.line, self.column
        value = ""
        # check leading negative sign
        if self.text[self.pos] == "-":
            value += "-"
            self.advance()
        # check number part
        if self.pos < len(self.text) and self.text[self.pos] == "0":
            value += "0"
            self.advance()
            if self.pos < len(self.text) and self.text[self.pos].isdigit():
                raise ValueError(
                    f"Leading zeroes not allowed at line {start_line}, column {start_column}"
                )
        elif self.pos < len(self.text) and self.text[self.pos].isdigit():
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                value += self.text[self.pos]
                self.advance()
        else:
            raise ValueError(
                f"Invalid number at line {start_line}, column {start_column}"
            )
        # check fraction part
        if self.pos < len(self.text) and self.text[self.pos] == ".":
            value += "."
            self.advance()
            if not (self.pos < len(self.text) and self.text[self.pos].isdigit()):
                raise ValueError(
                    f"Invalid fractional part at line {self.line}, column {self.column}"
                )
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                value += self.text[self.pos]
                self.advance()
        # check exponent part
        if self.pos < len(self.text) and self.text[self.pos] in "eE":
            value += self.text[self.pos]
            self.advance()
            if self.pos < len(self.text) and self.text[self.pos] in "-+":
                value += self.text[self.pos]
                self.advance()
            if not (self.pos < len(self.text) and self.text[self.pos].isdigit()):
                raise ValueError(
                    f"Invalid exponent part at line {self.line}, column {self.column}"
                )
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                value += self.text[self.pos]
                self.advance()

        return self.create_token(TokenType.NUMBER, value)

    def tokenize_keyword(self):
        value = ""
        while self.pos < len(self.text) and self.text[self.pos].isalpha():
            value += self.text[self.pos]
            self.advance()
        if value == "false" or value == "true":
            return self.create_token(TokenType.BOOLEAN, value)
        elif value == "null":
            return self.create_token(TokenType.NULL, value)
        else:
            raise ValueError(f"Invalid token at line {self.line}, column {self.column}")


def main():
    parser = argparse.ArgumentParser(
        prog="JSONParser",
        description="Give me some JSON, and I'll parse it.",
    )
    parser.add_argument("filename")
    args = parser.parse_args()
    file_str = read_file(args.filename)
    lexer = JSONLexer(file_str)
    tokens = lexer.tokenize()
    print_sandwich(f"⭐️ Parsed {len(tokens)} tokens ⭐️")
    for t in tokens:
        print(t)


if __name__ == "__main__":
    main()
