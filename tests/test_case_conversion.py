# -*- coding: utf-8 -*-
import os
import unittest
from typing import List, Dict


from camelback.case_converter import CaseStyleEnum, case_convert_to_style, case_convert_stream, case_convert, get_casing_style


class TestCaseConversion(unittest.TestCase):
    SNAKE_CASE_FILE = os.path.join(os.path.dirname(__file__), 'bin', 'snakecase.c')
    MACRO_CASE_FILE = os.path.join(os.path.dirname(__file__), 'bin', 'macrocase.c')
    CAMEL_CASE_FILE = os.path.join(os.path.dirname(__file__), 'bin', 'camelcase.c')
    PASCAL_CASE_FILE = os.path.join(os.path.dirname(__file__), 'bin', 'pascalcase.c')

    STYLES = {
        CaseStyleEnum.SNAKE_CASE: ['m_t', 'my_token'],
        CaseStyleEnum.MACRO_CASE: ['M_T', 'MY_TOKEN'],
        CaseStyleEnum.CAMEL_CASE: ['mT', 'myToken'],
        CaseStyleEnum.PASCAL_CASE: ['MT', 'MyToken'],
    }

    def test_convert_to_current_format(self):
        # Given I read a file in snake case
        with open(TestCaseConversion.SNAKE_CASE_FILE) as f:
            original_stream = f.read()
        # If I convert it to snake case
        converted_stream = case_convert_stream(original_stream, CaseStyleEnum.SNAKE_CASE)
        # Then I should get a stream identical to the input file
        self.assertEqual(original_stream, converted_stream)

    def test_convert_to_different_format(self):
        # Given I read a file in snake case
        with open(TestCaseConversion.SNAKE_CASE_FILE) as f:
            original_stream = f.read()
        # If I convert it to macro case
        converted_stream = case_convert_stream(original_stream, CaseStyleEnum.MACRO_CASE)
        # Then I should get a stream identical to the input file in macro case
        with open(TestCaseConversion.MACRO_CASE_FILE) as f:
            expected_stream = f.read()
        self.assertEqual(expected_stream, converted_stream)

    def test_detect_casing_style(self):
        for correct_style, tokens in TestCaseConversion.STYLES.items():
            for token in tokens:
                print(correct_style, token)
                self.assertEqual(correct_style, get_casing_style(token))

    def _test_case_convert_across_set(self, case_set: Dict[CaseStyleEnum, List[str]]):
        for from_style, original_tokens in case_set.items():
            for to_style, correct_tokens in case_set.items():
                for i, original_token in enumerate(original_tokens):
                    correct_token = correct_tokens[i]
                    print(f'{original_token} -> {to_style.name} yes {correct_token} got ', end='')
                    converted_token = case_convert(original_token, to_style)
                    print(f'{converted_token}')

                    self.assertEqual(correct_token, converted_token)

    def test_case_convert_common(self):
        self._test_case_convert_across_set(TestCaseConversion.STYLES)

    def test_case_convert_edge_cases(self):
        edge_cases = {
            x: y for x, y in zip(
                (x for x in CaseStyleEnum), [
                    ['_', 'my_tok_', '_my_tok_', 'lots_of_words'],
                    ['_', 'MY_TOK_', '_MY_TOK_', 'LOTS_OF_WORDS'],
                    ['_', 'myTok_',  'My_tok_',  'lotsOfWords'],
                    ['_', 'MyTok_',  '_MyTok',  'LotsOfWords']
                ])
        }
        self._test_case_convert_across_set(edge_cases)
        # Currently this will fail: _my_tok_ to camel case. Should give _myTok, gives My_tok_

    def test_edge(self):
        print(case_convert('int', CaseStyleEnum.MACRO_CASE))
