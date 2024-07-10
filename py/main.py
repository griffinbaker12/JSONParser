import argparse

from analyzer import parse
from common import read_file
from lexer import JSONLexer


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
    print(f"Parsed {len(tokens)} tokens")

    # now take these tokens and feed to analyzer
    parse(tokens)
