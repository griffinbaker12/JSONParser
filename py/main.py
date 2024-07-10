import argparse

from analyzer import parse_tokens
from common import print_sandwich, read_file
from lexer import JSONLexer


def main():
    parser = argparse.ArgumentParser(
        prog="JSONParser",
        description="Give me some JSON, and I'll parse it.",
    )
    parser.add_argument("filename")
    args = parser.parse_args()

    # read file contents
    file_str = read_file(args.filename)

    # lex file into tokens
    lexer = JSONLexer(file_str)
    tokens = lexer.tokenize()
    print_sandwich(f"⭐️ Parsed {len(tokens)} tokens ⭐️")
    for t in tokens:
        print(t)

    # now take these tokens and feed to analyzer
    parsed = parse_tokens(tokens)
    print_sandwich("Parsed Result")
    print(parsed)
