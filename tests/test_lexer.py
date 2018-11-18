import os
import unittest

from camelback.lexer import Lexer


class TestLexer(unittest.TestCase):
    SOURCE_CODE_FILE = os.path.join(os.path.dirname(__file__), 'bin', 'snakecase.c')

    def test_tokenize_source_code(self):
        with open(TestLexer.SOURCE_CODE_FILE) as f:
            stream = f.read()
        lexer = Lexer(stream)

        tokens = []
        while True:
            try:
                tok = lexer.get()
                tokens.append(tok)
            except EOFError:
                break

        correct = ['#include', ' ', '<stdio.h>', ' ', ' ', '//', ' ', 'printf', '\n',
                   '\n',
                   'void', ' ', 'foo_bar', '(', 'int', ' ', 'user_argument', ')', ' ', '{', '\n',
                   ' ', ' ', ' ', ' ', 'printf', '(', '"%d\\n",', ' ', 'user_argument', ')', ';', '\n',
                   '}', '\n',
                   '\n',
                   'int', ' ', 'main', '(', 'int', ' ', 'argc,', ' ', 'char**', ' ', 'argv', ')', ' ', '{', '\n',
                   ' ', ' ', ' ', ' ', 'int', ' ', 'my_variable', ' ', '=', ' ', '42;', '\n',
                   ' ', ' ', ' ', ' ', 'foo_bar', '(', 'my_variable', ')', ';', '\n',
                   ' ', ' ', ' ', ' ', 'return', ' ', '0;', '\n',
                   '}',
                   '\n']
        self.assertEqual(correct, tokens)
