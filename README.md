# camelback

camelback is a Python utility to convert all identifiers in a source file between different casing styles.

The supported styles are:

* `snake_case`
* `MACRO_CASE`
* `camelCase`
* `PascalCase`

# Usage

## As a CLI tool

`$ python3 camelback-cli.py source_code.c SNAKE_CASE`

## As a library

```python
import os
from camelback.case_converter import CaseStyleEnum, case_convert_stream

directory = os.path.join(os.path.dirname(__file__), 'source_code_files')
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    with open(path, 'r') as f:
        original_contents = f.read()
    new_contents = case_convert_stream(original_contents, CaseStyleEnum.CAMEL_CASE)
    with open(path, 'w') as f:
        f.write(new_contents)
```

Requirements: 

> Anyone know a utility that can automatically change all identifiers’ case/underscore style for a whole file?  e.g. converting between FOO_BAR, fooBar, foo_bar, FooBar.

Additional requirement: You should not need to input the source file's case style, it should be automatically detected.


License
-----------------
MIT
