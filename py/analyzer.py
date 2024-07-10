import argparse

from common import print_sandwich, read_file
from lexer import JSONLexer, Token, TokenType

VALID_ARR_VALUES = [
    TokenType.STRING,
    TokenType.NUMBER,
    TokenType.BOOLEAN,
    TokenType.NULL,
]


def parse_array(tokens, start_idx=0):
    """
    Returns Python array with individual elements
    """
    if not tokens:
        raise ValueError("Expected closing ']'.")

    parsed_array = []

    # HAVE TO TRACK HOW FAR YOU WENT IN THE NESTED STRUCTURE
    curr_idx = start_idx
    while curr_idx < len(tokens):
        curr_token = tokens[curr_idx]
        print(f"curr_token: {curr_token}")
        if curr_token.type == TokenType.RIGHT_BRACKET:
            return parsed_array, curr_idx + 1

        value, curr_idx = parse_value(tokens, curr_idx)
        parsed_array.append(value)

        # not sure how we are going to do this, because we don't want trailing commas
        if curr_idx < len(tokens) and tokens[curr_idx].type == TokenType.COMMA:
            curr_idx += 1

    raise ValueError("Expected closing ']'.")


def parse_value(tokens, start_idx):
    if start_idx >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[start_idx]

    if token.type == TokenType.LEFT_BRACKET:
        return parse_array(tokens, start_idx + 1)
    elif token.type in VALID_ARR_VALUES:
        return token.value, start_idx + 1
    else:
        raise ValueError(
            f"Unexpected token: {token.value} at line {token.line}, column {token.column}"
        )


def parse_tokens(tokens):
    parsed_v, end_idx = parse_value(tokens, 0)
    print(parsed_v)
    if end_idx != len(tokens):
        raise ValueError(
            f"Unexpected token after JSON document at line {tokens[end_idx].line}, column {tokens[end_idx].column}"
        )
    return parsed_v


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
    tokens = [
        Token(TokenType.LEFT_BRACKET, "[", 1, 1),
        Token(TokenType.NUMBER, 1, 1, 2),
        Token(TokenType.COMMA, ",", 1, 3),
        Token(TokenType.LEFT_BRACKET, "[", 1, 4),
        Token(TokenType.NUMBER, 3, 1, 5),
        Token(TokenType.RIGHT_BRACKET, "]", 1, 6),
        Token(TokenType.RIGHT_BRACKET, "]", 1, 7),
    ]
    print_sandwich(f"Feeding to analyzer")
    analyzed = parse_tokens(tokens)
    print_sandwich(analyzed)


if __name__ == "__main__":
    main()
