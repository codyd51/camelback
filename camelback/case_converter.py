import re
from enum import Enum
from camelback.lexer import Lexer


class CaseStyleEnum(Enum):
    SNAKE_CASE = 0
    MACRO_CASE = 1
    CAMEL_CASE = 2
    PASCAL_CASE = 3
    UNKNOWN_CASE = 4


def case_convert_stream(stream: str, case_style: CaseStyleEnum) -> str:
    """Process and return the stream, after converting every eligible token to the desired case_style.
    """
    lexer = Lexer(stream)
    converted_stream = []
    while True:
        try:
            tok = lexer.get()
            current_style = get_casing_style(tok)
            if current_style != CaseStyleEnum.UNKNOWN_CASE:
                tok = case_convert_to_style(tok, current_style, case_style)

            converted_stream.append(tok)
        except EOFError:
            break
    # rejoin tokens
    return ''.join(converted_stream)


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
        if contains_upper and not contains_lower:
            return CaseStyleEnum.MACRO_CASE

    if token[0].isupper():
        return CaseStyleEnum.PASCAL_CASE
    return CaseStyleEnum.CAMEL_CASE


def case_convert(token: str, desired_style: CaseStyleEnum) -> str:
    """Convert a token to desired_style, without knowing its casing beforehand.
    """
    current_style = get_casing_style(token)
    if current_style == CaseStyleEnum.UNKNOWN_CASE:
        # if we didn't detect a known style, return the token unchanged
        return token
    return case_convert_to_style(token, current_style, desired_style)


def case_convert_to_style(token: str, current_style: CaseStyleEnum, desired_style: CaseStyleEnum) -> str:
    """Return the provided token after transforming the case from current_style to desired_style.
    The behavior is undefined if the token is not actually in the style specified.
    """
    # XXX(PT): I am sure there is a better way to write this method. Think about it more.
    if current_style == desired_style:
        return token

    # simple transformations
    # checks for current/desired style pairs
    if current_style == CaseStyleEnum.SNAKE_CASE and desired_style == CaseStyleEnum.MACRO_CASE:
        # snake -> macro, uppercase everything
        return token.upper()
    elif current_style == CaseStyleEnum.MACRO_CASE and desired_style == CaseStyleEnum.SNAKE_CASE:
        # macro -> snake, lowercase everything
        return token.lower()
    elif current_style == CaseStyleEnum.CAMEL_CASE and desired_style == CaseStyleEnum.PASCAL_CASE:
        # camel -> pascal, uppercase first character
        return f'{token[0].upper()}{token[1:]}'
    elif current_style == CaseStyleEnum.PASCAL_CASE and desired_style == CaseStyleEnum.CAMEL_CASE:
        # pascal -> camel, lowercase first character
        return f'{token[0].lower()}{token[1:]}'

    # 2-step transformations
    elif desired_style == CaseStyleEnum.MACRO_CASE:
        # any -> macro, convert to snake then convert to actual
        snake_case = case_convert_to_style(token, current_style, CaseStyleEnum.SNAKE_CASE)
        return case_convert_to_style(snake_case, CaseStyleEnum.SNAKE_CASE, desired_style)
    elif desired_style == CaseStyleEnum.PASCAL_CASE:
        # any -> pascal, convert to camel then convert to pascal
        camel_case = case_convert_to_style(token, current_style, CaseStyleEnum.CAMEL_CASE)
        return case_convert_to_style(camel_case, CaseStyleEnum.CAMEL_CASE, desired_style)
    elif current_style == CaseStyleEnum.MACRO_CASE and desired_style == CaseStyleEnum.CAMEL_CASE:
        # macro -> camel, convert to snake then convert to camel
        snake_case = case_convert_to_style(token, current_style, CaseStyleEnum.SNAKE_CASE)
        return case_convert_to_style(snake_case, CaseStyleEnum.SNAKE_CASE, CaseStyleEnum.CAMEL_CASE)

    # transformations which require more logic
    elif current_style == CaseStyleEnum.SNAKE_CASE and desired_style == CaseStyleEnum.CAMEL_CASE:
        return _case_convert_snake_to_camel(token)
    elif desired_style == CaseStyleEnum.SNAKE_CASE:
        # we know that desired_style is one of the camel-cases because an earlier branch would have been taken
        return _case_convert_capital_to_snake(token)

    raise RuntimeError(f'unhandled conversion {current_style} to {desired_style}')


def _case_convert_snake_to_camel(token: str) -> str:
    """Implements logic to convert a snake case token to a camel case one.
    """
    while True:
        try:
            # find next underscore
            underscore_loc = token.index('_')
        except ValueError:
            # converted all underscores
            break
        # is the underscore at the end of the string?
        if underscore_loc == len(token) - 1:
            break

        orig = token
        token = f'{orig[:underscore_loc]}{orig[underscore_loc+1].upper()}'
        # is there more after the capital?
        if len(orig) > underscore_loc+2:
            token += f'{orig[underscore_loc+2:]}'
    return token


def _case_convert_capital_to_snake(token: str) -> str:
    """Implements logic to convert a camel or Pascal case token to a snake case one.
    """
    # split on uppercase characters
    # this split works by inserting a space before each uppercase character, then space-splitting
    components = re.sub(r'([A-Z])', r' \1', token).split()
    return '_'.join(components).lower()
