import unittest

from .lexer import JSONLexer, TokenType


class TestJSONLexer(unittest.TestCase):
    def test_basic_tokens(self):
        lexer = JSONLexer("{}")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.LEFT_BRACE)
        self.assertEqual(tokens[1].type, TokenType.RIGHT_BRACE)

    def test_string_tokenization(self):
        test_cases = [
            ('"Simple string"', '"Simple string"'),
            ('"Escape \\"quotes\\""', '"Escape \\"quotes\\""'),
            ('"Unicode \\u00A9"', '"Unicode \\u00A9"'),
            (
                '"Escape sequences \\b\\f\\n\\r\\t"',
                '"Escape sequences \\b\\f\\n\\r\\t"',
            ),
            (
                '"Invalid escape \\x"',
                '"Invalid escape \\x"',
            ),
        ]
        for input_str, expected_value in test_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 1)
                self.assertEqual(tokens[0].type, TokenType.STRING)
                self.assertEqual(tokens[0].value, expected_value)

    def test_invalid_strings(self):
        invalid_cases = [
            '"Unterminated string',
            '"Invalid Unicode \\u12XY"',
            '"Unescaped control character \u0000"',  # Using an actual control character
        ]
        for input_str in invalid_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                with self.assertRaises(ValueError):
                    lexer.tokenize()

    def test_whitespace_handling(self):
        lexer = JSONLexer("  \t\n\r{ \n\t}")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.LEFT_BRACE)
        self.assertEqual(tokens[0].line, 2)  # After the newline
        self.assertEqual(tokens[1].type, TokenType.RIGHT_BRACE)
        self.assertEqual(tokens[1].line, 3)  # On the third line


if __name__ == "__main__":
    unittest.main()
