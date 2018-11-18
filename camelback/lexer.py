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
            raise EOFError
        return self._tokens[self._token_index]

    def get(self) -> str:
        """Read and consume the next token in the stream
        """
        tok = self.peek()
        self._token_index += 1
        return tok

    @staticmethod
    def _split_stream(stream: str) -> List[str]:
        """Tokenize a raw stream.
        """
        return [x for x in re.split(r'(\s|\(|\)+)', stream) if len(x)]
