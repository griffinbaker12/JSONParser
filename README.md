# Inspiration
I've always wanted to understand how parsing works.

# Reference
This [site](https://notes.eatonphil.com/writing-a-simple-json-parser.html) was good to understand how to initially think about the problem. Their implementation is too simple, but it gets you off the ground.
Once I understood the basic premise, this [site](https://www.crockford.com/mckeeman.html) was super helpful as it has the complete JSON grammar.
At that point, it pretty much becomes translating the grammar into the PL of your choice.

# Capabilities and Testing
This parser isn't perfect, but I wanted to push it beyond just basic examples. For example, it can accurately parse:

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

You can add addtionaal tests to to ```test/``` directory, and run them via:

```
python -m unittest py/test_parser.py
```

This [site](https://jsonlint.com/) was also helpful in visualizing different test cases.

# Notes
Two parts to the parsing process:
1) Lexical analysis -> split input into tokens
2) Syntactic analysis -> gets fed the tokens to validate syntactical patterns

There's nothing magic about this process, which, I guess, makes it kind of magic.
