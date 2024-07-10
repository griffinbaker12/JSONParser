# JSON Parser in Python

An implementation of a JSON Parser in Python. This parser performs both lexical and syntactic analysis of JSON input, providing detailed error reporting with line and column numbers if parsing fails.

## Inspiration

I've always wanted to understand how parsing works!

## Features

- Full JSON syntax support
- Detailed error reporting with line and column numbers
- Handles nested structures and all JSON data types
- Extensive test suite

## Usage

```bash
python3 py/json-parser FILE
```

## Testing

Add any additional tests to the `test/` directory you may want, then run:

```bash
python3 -m unittest py/test_parser.py
```

## Capabilities

This parser can handle complex JSON structures, including nested objects and arrays, Unicode characters, and escape sequences. Here's an example of a complex JSON it can parse:

```
[
    "JSON Test Pattern pass1",
    {
        "object with 1 member": [
            "array with 1 element"
        ]
    },
    {},
    [],
    -42,
    true,
    false,
    null,
    {
        "integer": 1234567890,
        "real": -9876.54321,
        "e": 1.23456789e-13,
        "E": 1.23456789e+34,
        "": 2.3456789012e+76,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "controls": "\b\f\n\r\t",
        "slash": "/ & \/",
        "alpha": "abcdefghijklmnopqrstuvwyz",
        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
        "digit": "0123456789",
        "0123456789": "digit",
        "special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
        "hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
        "true": true,
        "false": false,
        "null": null,
        "array": [],
        "object": {},
        "address": "50 St. James Street",
        "url": "http://www.JSON.org/",
        "comment": "// /* <!-- --",
        "# -- --> */": " ",
        " s p a c e d ": [
            1,
            2,
            3,
            4,
            5,
            6,
            7
        ],
        "compact": [
            1,
            2,
            3,
            4,
            5,
            6,
            7
        ],
        "jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
        "quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
        "\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?": "A key can be any string"
    },
    0.5,
    98.6,
    99.44,
    1066,
    10,
    1,
    0.1,
    1,
    2,
    2,
    "rosebud"
]
```

## References

- [Writing a Simple JSON Parser](https://notes.eatonphil.com/writing-a-simple-json-parser.html) - Helpful for understanding initial concepts.
- [JSON Grammar](https://www.crockford.com/mckeeman.html) - Comprehensive JSON grammar reference.
- [JSONLint](https://jsonlint.com/) - Useful for visualizing and validating JSON.

## Notes on Parsing Process

Two parts to the parsing process:
1) Lexical analysis -> split input into tokens
2) Syntactic analysis -> gets fed the tokens to validate syntactical patterns

There's nothing magic about this process, which, I guess, makes it kind of magic.
