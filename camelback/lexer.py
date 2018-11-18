# -*- coding: utf-8 -*-
import re
from typing import List, Optional


class LexingError(Exception):
    pass


class Lexer(object):
    """Base class for tokenizing a file and reading the token stream
    """
    def __init__(self, contents: str):
        self.contents = contents
        self._tokens = self._split_stream(self.contents)
        self._token_index = 0

    def peek(self) -> Optional[str]:
        """Read the next token in the stream, without consuming it
        """
        if self._token_index >= len(self._tokens):
            return None
        return self._tokens[self._token_index]

    def get(self) -> str:
        """Read and consume the next token in the stream
        """
        tok = self.peek()
        self._token_index += 1
        return tok

    def match(self, expected: str):
        """Consume the next token, and verify it matches an expected value
        This method will throw a ParseError if the next token did not match the expected value
        """
        real_tok = self.get()
        if real_tok != expected:
            raise LexingError('Expected token {}, got {}'.format(repr(expected), repr(real_tok)))

    @staticmethod
    def _split_stream(stream: str) -> List[str]:
        """Tokenize a raw stream.
        """
        return re.findall(r"[\w']+|[*+@.,!#?;():/\-\[\]\n\"\\]", stream)

    def match_str(self, expected: str) -> None:
        """Given a source string, tokenize it and ensure the token stream matches those tokens exactly.
        Also consumes the tokens.
        """
        expected_stream = self._split_stream(expected)
        for expected_tok in expected_stream:
            try:
                self.match(expected_tok)
            except LexingError as e:
                raise LexingError(f'Matching string {expected_stream} failed! {str(e)}')
