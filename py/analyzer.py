import argparse
from typing import Dict, List, Tuple, TypeVar, Union

from common import print_sandwich, read_file
from lexer import JSONLexer, Token, TokenType

VALID_ARR_VALUES = [
    TokenType.STRING,
    TokenType.NUMBER,
    TokenType.BOOLEAN,
    TokenType.NULL,
]

JSONValue = Union[str, int, float, bool, None, List["JSONValue"], "JSONObject"]
JSONObject = Dict[str, JSONValue]
JSONKey = TypeVar("JSONKey", bound=str)


def parse_array(tokens: List[Token], start_idx=0) -> Tuple[List[Token], int]:
    """
    Returns Python array with individual elements and next index to be parsed.
    """
    if not tokens:
        raise ValueError("Expected closing ']'.")

    parsed_array = []

    # HAVE TO TRACK HOW FAR YOU WENT IN THE NESTED STRUCTURE
    curr_idx = start_idx
    while curr_idx < len(tokens):
        curr_token = tokens[curr_idx]
        if curr_token.type == TokenType.RIGHT_BRACKET:
            return parsed_array, curr_idx + 1

        value, curr_idx = parse_value(tokens, curr_idx)
        parsed_array.append(value)

        if curr_idx < len(tokens) and tokens[curr_idx].type == TokenType.COMMA:
            peak_idx = curr_idx + 1
            if peak_idx == len(tokens):
                raise ValueError(
                    f"Expected another array element at line {tokens[curr_idx].line}, column {tokens[curr_idx].column}"
                )
            peaked = tokens[peak_idx]
            if peaked.type == TokenType.RIGHT_BRACKET:
                raise ValueError(
                    f"Invalid trailing comma at end of the array at line {peaked.line}, column, {peaked.column}"
                )
            curr_idx += 1

    raise ValueError("Expected closing ']'.")


def parse_object(tokens: List[Token], start_idx=0) -> Tuple[JSONObject, int]:
    """
    Returns Python object with individual elements and next index to be parsed.
    """
    if not tokens:
        raise ValueError("Expected closing ']'.")

    parsed_obj = {}

    curr_idx = start_idx
    while curr_idx < len(tokens):
        curr_token = tokens[curr_idx]
        if curr_token.type == TokenType.RIGHT_BRACE:
            return parsed_obj, curr_idx + 1

        if curr_token.type != TokenType.STRING:
            raise ValueError(
                f"Expected string key at line {tokens[curr_idx].line}, column {tokens[curr_idx].column}"
            )

        key = token_to_type(curr_token)
        curr_idx += 1

        if curr_idx == len(tokens) or tokens[curr_idx].type != TokenType.COLON:
            raise ValueError(
                f"Expected ':' at line {tokens[curr_idx].line}, column {tokens[curr_idx].column}"
            )
        curr_idx += 1

        # now lets get the parsed value, and append to dict
        value, curr_idx = parse_value(tokens, curr_idx)

        parsed_obj[key] = value

        if curr_idx < len(tokens) and tokens[curr_idx].type == TokenType.COMMA:
            peak_idx = curr_idx + 1
            if peak_idx == len(tokens):
                raise ValueError(
                    f"Expected another dictionary element at line {tokens[curr_idx].line}, column {tokens[curr_idx].column}"
                )
            peaked = tokens[peak_idx]
            if peaked.type == TokenType.RIGHT_BRACKET:
                raise ValueError(
                    f"Invalid trailing comma at end of the array at line {peaked.line}, column, {peaked.column}"
                )
            curr_idx += 1

    raise ValueError("Expected closing '}'.")


def parse_value(tokens: List[Token], start_idx):
    if start_idx >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[start_idx]

    if token.type == TokenType.LEFT_BRACKET:
        return parse_array(tokens, start_idx + 1)
    elif token.type == TokenType.LEFT_BRACE:
        return parse_object(tokens, start_idx + 1)
    elif token.type in VALID_ARR_VALUES:
        return token_to_type(token), start_idx + 1
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


def token_to_type(token: Token):
    v, t = token.value, token.type
    print(v)
    if t == TokenType.BOOLEAN:
        return token.value == "true"
    elif t == TokenType.NULL:
        return None
    elif t == TokenType.NUMBER:
        return int(v) if v.isdigit() else float(v)
    elif t == TokenType.STRING:
        return v.strip('"')
    else:
        return v


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
    print_sandwich(f"Feeding to analyzer")
    analyzed = parse_tokens(tokens)
    print_sandwich(f"Parsed Result")
    print(analyzed)


if __name__ == "__main__":
    main()
