# -*- coding: utf-8 -*-
import os
import unittest


from camelback.case_converter import CaseStyleEnum, CaseConverter


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
        converter = CaseConverter(original_stream)
        converted_stream = converter.convert(CaseStyleEnum.SNAKE_CASE)
        # Then I should get a stream identical to the input file
        self.assertEqual(original_stream, converted_stream)

    def test_convert_to_different_format(self):
        # Given I read a file in snake case
        with open(TestCaseConversion.SNAKE_CASE_FILE) as f:
            original_stream = f.read()
        # If I convert it to macro case
        converter = CaseConverter(original_stream)
        converted_stream = converter.convert(CaseStyleEnum.MACRO_CASE)
        # Then I should get a stream identical to the input file in macro case
        with open(TestCaseConversion.MACRO_CASE_FILE) as f:
            expected_stream = f.read()
        self.assertEqual(expected_stream, converted_stream)

    def test_detect_casing_style(self):
        for correct_style, tokens in TestCaseConversion.STYLES.items():
            for token in tokens:
                print(correct_style, token)
                self.assertEqual(correct_style, CaseConverter.get_casing_style(token))

    def test_convert_case(self):
        for from_style, original_tokens in TestCaseConversion.STYLES.items():
            for to_style, correct_tokens in TestCaseConversion.STYLES.items():
                for i, original_token in enumerate(original_tokens):
                    correct_token = correct_tokens[i]

                    print(f'{original_token} to {to_style.name}. Expect {correct_token}, got ', end='')
                    converted_token = CaseConverter.convert_style(original_token, from_style, to_style)
                    print(converted_token)

                    self.assertEqual(correct_token, converted_token)
