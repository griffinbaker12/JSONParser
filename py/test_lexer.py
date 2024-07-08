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
            ('"Valid escape \\\\x"', '"Valid escape \\\\x"'),
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
            '"Unescaped control character \0"',
            '"Invalid escape \\x"',
        ]
        for input_str in invalid_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                with self.assertRaises(ValueError):
                    lexer.tokenize()

    def test_valid_control_character_escapes(self):
        valid_cases = [
            ('"Valid escape \\u0000"', '"Valid escape \\u0000"'),
            ('"Valid escape \\u001F"', '"Valid escape \\u001F"'),
        ]
        for input_str, expected_value in valid_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 1)
                self.assertEqual(tokens[0].type, TokenType.STRING)
                self.assertEqual(tokens[0].value, expected_value)

    def test_whitespace_handling(self):
        lexer = JSONLexer("  \t\n\r{ \n\t}")
        tokens = lexer.tokenize()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.LEFT_BRACE)
        self.assertEqual(tokens[0].line, 2)  # After the newline
        self.assertEqual(tokens[1].type, TokenType.RIGHT_BRACE)
        self.assertEqual(tokens[1].line, 3)  # On the third line

    def test_integer_tokenization(self):
        test_cases = [
            ("0", "0"),
            ("123", "123"),
            ("-456", "-456"),
            ("1000000", "1000000"),
            ("-0", "-0"),
        ]
        for input_str, expected_value in test_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 1)
                self.assertEqual(tokens[0].type, TokenType.NUMBER)
                self.assertEqual(tokens[0].value, expected_value)

    def test_float_tokenization(self):
        test_cases = [
            ("0.123", "0.123"),
            ("-3.14", "-3.14"),
            ("2.0e10", "2.0e10"),
            ("-1.23E-4", "-1.23E-4"),
        ]
        for input_str, expected_value in test_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 1)
                self.assertEqual(tokens[0].type, TokenType.NUMBER)
                self.assertEqual(tokens[0].value, expected_value)

    def test_invalid_numbers(self):
        invalid_cases = [
            "01",
            "-01",
            "1.",
            ".1",
            "1e",
            "1e+",
            "1E-",
            "1.2.3",
            "1e2.3",
            "1e+2.3",
            "--1",
            "+-1",
            "1e+-2",
            "1e2e3",
            "0x123",
            "Infinity",
            "NaN",
        ]
        for input_str in invalid_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                with self.assertRaises(ValueError):
                    lexer.tokenize()

    def test_keyword_tokenization(self):
        test_cases = [
            ("true", TokenType.BOOLEAN, "true"),
            ("false", TokenType.BOOLEAN, "false"),
            ("null", TokenType.NULL, "null"),
        ]
        for input_str, expected_type, expected_value in test_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                tokens = lexer.tokenize()
                self.assertEqual(len(tokens), 1)
                self.assertEqual(tokens[0].type, expected_type)
                self.assertEqual(tokens[0].value, expected_value)

    def test_invalid_keywords(self):
        invalid_cases = [
            "True",  # Uppercase T
            "FALSE",  # All uppercase
            "Null",  # Uppercase N
            "undefined",  # Not a JSON keyword
        ]
        for input_str in invalid_cases:
            with self.subTest(input=input_str):
                lexer = JSONLexer(input_str)
                with self.assertRaises(ValueError):
                    lexer.tokenize()


if __name__ == "__main__":
    unittest.main()
