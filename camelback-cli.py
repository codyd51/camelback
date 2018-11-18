# -*- coding: utf-8 -*-
import os
import sys
import argparse

from camelback.case_converter import CaseStyleEnum, case_convert_stream


def convert_file_case(path: str, style: CaseStyleEnum) -> None:
    with open(path, 'r') as f:
        contents = f.read()
    new_contents = case_convert_stream(contents, style)
    with open(path, 'w') as f:
        f.write(new_contents)


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert casing styles of files')
    parser.add_argument(
        'case_style', type=str, help=
        'The desired casing style. Options are SNAKE_CASE, MACRO_CASE, CAMEL_CASE, PASCAL_CASE'
    )
    parser.add_argument(
        'input_files', type=str, nargs='+', help=
        'One or more files whose casing style should be converted'
    )
    args = parser.parse_args()

    # ensure a valid case_style was provided
    try:
        desired_style = CaseStyleEnum[args.case_style]
        if desired_style == CaseStyleEnum.UNKNOWN_CASE:
            # internal casing style that should not be specified at CLI
            raise RuntimeError()
    except (KeyError, RuntimeError):
        print(f'Invalid casing style {args.case_style}.')
        print(f'Valid options are SNAKE_CASE, MACRO_CASE, CAMEL_CASE, PASCAL_CASE.')
        sys.exit(0)

    for input_file in args.input_files:
        if not os.path.exists(input_file):
            print(f'No such file: {input_file}.')
            continue
        convert_file_case(input_file, desired_style)
        print(f'Converted {input_file} to {desired_style.name}.')


if __name__ == '__main__':
    main()
