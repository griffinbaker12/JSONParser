# Inspiration
I've always wanted to understand how parsing works.

# Reference
This [site](https://notes.eatonphil.com/writing-a-simple-json-parser.html) was good to understand how to initially think about the problem. Their implementation is too simple, but it gets you off the ground.
Once I understood the basic premise, this [site](https://www.crockford.com/mckeeman.html) was super helpful as it has the complete JSON grammar.
At that point, it pretty much becomes copying the grammar into the PL of your choice.

# Test Cases
I added a pretty comprehensive test suite (to the lexer only thus far), which you can run with the following command:

'''
python -m unittest py/test_lexer.py
'''

This [site](https://jsonlint.com/) was also helpful in visualizing different test cases.

# Notes
Two parts to the parsing process:
1) Lexical analysis -> split input into tokens
2) Syntactic analysis -> gets fed the tokens to find patterns to meet lang spec

There's nothing magic about this process, which, I guess, makes it kind of magic.
