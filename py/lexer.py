import argparse
from enum import Enum, auto

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
                tokens.append(self.tokenize_boolean())
            else:
                raise ValueError(f"Unexpected character: {char} at position {self.pos}")
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
                if self.pos < len(self.text):
                    next_char = self.text[self.pos]
                    value += next_char
                    self.advance()
                    if next_char == "u":
                        # Validate the next 4 characters as hex digits
                        for _ in range(4):
                            if (
                                self.pos < len(self.text)
                                and self.text[self.pos] in "0123456789ABCDEFabcdef"
                            ):
                                value += self.text[self.pos]
                                self.advance()
                            else:
                                raise ValueError(
                                    f"Invalid Unicode escape sequence at line {self.line}, column {self.column}"
                                )
                else:
                    raise ValueError(
                        f"Unterminated string at line {start_line}, column {start_column}"
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
        pass

    def tokenize_boolean(self):
        pass


def read_file(json_file):
    with open(json_file) as f:
        json_content = f.read()
    return json_content


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
    print(tokens)


if __name__ == "__main__":
    main()
