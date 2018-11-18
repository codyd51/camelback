import re
from enum import Enum
from camelback.lexer import Lexer


class CaseStyleEnum(Enum):
    SNAKE_CASE = 0
    MACRO_CASE = 1
    CAMEL_CASE = 2
    PASCAL_CASE = 3
    UNKNOWN_CASE = 4


class CaseConverter:
    def __init__(self, stream: str):
        self.input_stream = stream
        self.lexer = Lexer(stream)

    def convert(self, case_style: CaseStyleEnum) -> str:
        converted_stream = []
        while True:
            try:
                tok = self.lexer.get()
                tok = self._convert_tok(tok, case_style)
                converted_stream.append(tok)
            except EOFError:
                break
        # rejoin tokens
        return ''.join(converted_stream)

    @staticmethod
    def snake_to_camel(token: str):
        components = token.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def get_casing_style(token: str) -> CaseStyleEnum:
        # make sure token is long enough to have casing
        if len(token) < 2:
            return CaseStyleEnum.UNKNOWN_CASE
        # make sure token is an identifier
        if not token[0].isalpha():
            return CaseStyleEnum.UNKNOWN_CASE
def get_casing_style(token: str) -> CaseStyleEnum:
    """Return the case style of the provided token.

    If the token does not have a definitive casing, UNKNOWN_CASE is returned.
    """
    # make sure token is long enough to have casing
    if len(token) < 2:
        return CaseStyleEnum.UNKNOWN_CASE
    # make sure token is an identifier
    # variables/function names typically can begin either with an alpha or underscore
    if not token[0].isalpha() and token[0] != '_':
        return CaseStyleEnum.UNKNOWN_CASE

    # make sure token has upper or lowercase characters
    contains_upper = any(x.isupper() for x in token)
    contains_lower = any(x.islower() for x in token)
    if not contains_upper and not contains_lower:
        return CaseStyleEnum.UNKNOWN_CASE

    # make sure the token either contains uppercase characters or an underscore
    # otherwise, it doesn't have definitive casing
    if not contains_upper and '_' not in token:
        return CaseStyleEnum.UNKNOWN_CASE

    if '_' in token:
        if contains_upper and contains_lower:
            return CaseStyleEnum.UNKNOWN_CASE
        if contains_lower and not contains_upper:
            return CaseStyleEnum.SNAKE_CASE
        return CaseStyleEnum.CAMEL_CASE

    def _convert_tok(self, token: str, desired_style: CaseStyleEnum) -> str:
        current_style = self.get_casing_style(token)
        if current_style == CaseStyleEnum.UNKNOWN_CASE:
            # if we didn't detect a known style, return the token unchanged
            return token
        return self.convert_style(token, current_style, desired_style)

    @staticmethod
    def convert_style(token: str, current_style: CaseStyleEnum, desired_style: CaseStyleEnum) -> str:
        """Recursively transform the input string from the original style to the desired style.
        """
        # XXX(PT): I am sure there is a better way to write this method. Think about it more.
        if current_style == desired_style:
            return token

        # simple cases
        if current_style == CaseStyleEnum.SNAKE_CASE:
            if desired_style == CaseStyleEnum.MACRO_CASE:
                # snake -> macro, uppercase everything
                return token.upper()
        elif current_style == CaseStyleEnum.MACRO_CASE:
            if desired_style == CaseStyleEnum.SNAKE_CASE:
                # macro -> snake, lowercase everything
                return token.lower()
            elif desired_style == CaseStyleEnum.CAMEL_CASE:
                # macro -> camel, convert to snake then convert to camel
                snake_case = CaseConverter.convert_style(token, current_style, CaseStyleEnum.SNAKE_CASE)
                return CaseConverter.convert_style(snake_case, CaseStyleEnum.SNAKE_CASE, CaseStyleEnum.CAMEL_CASE)
        elif current_style == CaseStyleEnum.CAMEL_CASE:
            if desired_style == CaseStyleEnum.PASCAL_CASE:
                # camel -> pascal, uppercase first character
                return f'{token[0].upper()}{token[1:]}'
        elif current_style == CaseStyleEnum.PASCAL_CASE:
            if desired_style == CaseStyleEnum.CAMEL_CASE:
                # pascal -> camel, lowercase first character
                return f'{token[0].lower()}{token[1:]}'

        if desired_style == CaseStyleEnum.MACRO_CASE:
            # in the general case, convert to macro by converting to snake then converting snake to macro
            snake_case = CaseConverter.convert_style(token, current_style, CaseStyleEnum.SNAKE_CASE)
            return CaseConverter.convert_style(snake_case, CaseStyleEnum.SNAKE_CASE, desired_style)
        if desired_style == CaseStyleEnum.PASCAL_CASE:
            # in the general case, convert to pascal by converting to camel then converting to pascal
            camel_case = CaseConverter.convert_style(token, current_style, CaseStyleEnum.CAMEL_CASE)
            return CaseConverter.convert_style(camel_case, CaseStyleEnum.CAMEL_CASE, desired_style)

        if desired_style == CaseStyleEnum.CAMEL_CASE:
            if current_style == CaseStyleEnum.SNAKE_CASE:
                try:
                    underscore_loc = token.index('_')
                except ValueError:
                    # converted all underscores
                    return token
                # TODO(PT): will this break when using strings ending in underscores?
                return f'{token[:underscore_loc]}{token[underscore_loc+1].upper()}{token[underscore_loc+2:]}'

        elif desired_style == CaseStyleEnum.SNAKE_CASE:
            if current_style in [CaseStyleEnum.CAMEL_CASE, CaseStyleEnum.PASCAL_CASE]:
                # split on uppercase characters
                # this split works by inserting a space before each uppercase character, then space-splitting
                components = re.sub(r'([A-Z])', r' \1', token).split()
                return '_'.join(components).lower()

        raise RuntimeError(f'unhandled conversion {current_style} to {desired_style}')
