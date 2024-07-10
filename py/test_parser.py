import os
import unittest

from analyzer import parse_tokens
from lexer import JSONLexer


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        # Set up the path to the test files
        self.test_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test"
        )

    def test_pass_cases(self):
        pass_files = ["pass1.json", "pass2.json", "pass3.json", "pass4.json"]
        for file in pass_files:
            with self.subTest(file=file):
                file_path = os.path.join(self.test_dir, file)
                with open(file_path, "r") as f:
                    json_str = f.read()
                try:
                    lexer = JSONLexer(json_str)
                    tokens = lexer.tokenize()
                    parsed = parse_tokens(tokens)
                    self.assertIsNotNone(parsed)  # Ensure something was parsed
                except Exception as e:
                    self.fail(f"Parser raised {type(e).__name__} for {file}: {str(e)}")

    def test_fail_cases(self):
        fail_files = [
            f
            for f in os.listdir(self.test_dir)
            if f.startswith("fail") and f.endswith(".json")
        ]
        for file in fail_files:
            with self.subTest(file=file):
                file_path = os.path.join(self.test_dir, file)
                with open(file_path, "r") as f:
                    json_str = f.read()
                with self.assertRaises(
                    Exception, msg=f"Parser did not raise an exception for {file}"
                ):
                    lexer = JSONLexer(json_str)
                    tokens = lexer.tokenize()
                    parse_tokens(tokens)


if __name__ == "__main__":
    unittest.main()
