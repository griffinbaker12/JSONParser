import argparse
from enum import Enum, auto
from pprint import pprint

ESC_CHARS = [
    '"',
    "\\",
    "/",
    "b",
    "f",
    "n",
    "r",
    "t",
    "u",
]


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
                self.create_token(TokenType.LEFT_BRACE, "[")
                self.advance()
            elif char == "}":
                self.create_token(TokenType.RIGHT_BRACE, "]")
                self.advance()
            elif char == "[":
                self.create_token(TokenType.LEFT_BRACKET, "{")
                self.advance()
            elif char == "]":
                self.create_token(TokenType.RIGHT_BRACKET, "}")
                self.advance()
            elif char == ",":
                self.create_token(TokenType.COMMA, ",")
                self.advance()
            elif char == ".":
                self.create_token(TokenType.COLON, ":")
                self.advance()
            elif char == '"':
                tokens.append(self.tokenize_string())
            elif char.isdigit() or char == "-":
                tokens.append(self.tokenize_number())
            elif char.isalpha():
                tokens.append(self.tokenize_boolean())

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
        start_line, start_column = (
            self.line,
            self.column,
        )  # store where we started for when we create the Token
        self.advance()  # move past initial quote

        # we don't need to build up a new string, just raise error if something is invalid
        while not self.done_tokenizing():
            char = self.text[self.pos]
            # if we hit escape character
            if char == "\\":
                self.advance()
                if self.done_tokenizing():
                    raise ValueError(
                        f"Unterminated string beginning at line {start_line}, column {start_column}"
                    )

                esc_char = self.text[self.pos]
                if esc_char not in ESC_CHARS:
                    raise ValueError(
                        f"Invalid escape sequence '\\{esc_char}' at line {self.line}, column {self.column}"
                    )
                if esc_char == "u":
                    # inc for len of hex_string
                    for _ in range(4):
                        self.advance()
                    if self.done_tokenizing():
                        raise ValueError(
                            f"Invalid hex sequence at line {self.line}, column {self.column - 4}"
                        )
                    hex_seq = self.text[self.pos - 3 : self.pos + 1]
                    if not all(
                        c in (valid_hex := "0123456789ABCEDFabcedf") for c in hex_seq
                    ):
                        reset_col = self.column - 4
                        for c_ in hex_seq:
                            if c_ not in valid_hex:
                                raise ValueError(
                                    f"Invalid hex sequence at line {self.line}, column {reset_col}"
                                )
                            else:
                                reset_col += 1
            elif not (0x20 <= ord(char) <= 0x10FFFF):
                raise ValueError(
                    f"Invalid character {char} in string at line {self.line}, column {self.column}"
                )

    def done_tokenizing(self):
        return self.pos >= len(self.text) or self.text[self.pos] == '"'

    def tokenize_number(self):
        pass

    def tokenize_boolean(self):
        pass

    # def tokenize(self):
    #     print("Working on text of length:", len(self.text))
    #     tokens = []
    #     while self.pos < len(self.text):
    #         char = self.text[self.pos]
    #         if char == "{":
    #             tokens.append(Token())
    #     return tokens


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
    print(file_str)
    lexer = JSONLexer(file_str)
    # tokens = lexer.tokenize()
    # pprint(tokens)


if __name__ == "__main__":
    main()
