# camelback

camelback is a Python utility to convert all identifiers in a source file between different casing styles.

Inspired by [this tweet.](https://twitter.com/comex/status/1062814338182868992)

The supported options for casing styles:

* `SNAKE_CASE`: `foo_bar`
* `MACRO_CASE`: `FOO_BAR`
* `CAMEL_CASE`: `fooBar`
* `PASCAL_CASE`: `FooBar`

## Example

```
$ cat code.c
#include <stdio.h>  // printf
void FOO_BAR(int USER_ARGUMENT) {
    printf("%d\n", USER_ARGUMENT);
}
int main(int argc, char** argv) {
    int MY_VARIABLE = 42;
    FOO_BAR(MY_VARIABLE);
    return 0;
}
$ python3 CAMEL_CASE code.c code.h
Converted code.c to CAMEL_CASE
Converted code.h to CAMEL_CASE
$ cat code.c
#include <stdio.h>  // printf
void fooBar(int userArgument) {
    printf("%d\n", userArgument);
}
int main(int argc, char** argv) {
    int myVariable = 42;
    fooBar(myVariable);
    return 0;
}
```

## Usage

### As a CLI tool

`$ python3 camelback-cli.py SNAKE_CASE source_code.h source_code.c`

### As a library

```python
import os
from camelback.case_converter import CaseStyleEnum, case_convert_file

directory = os.path.join(os.path.dirname(__file__), 'source_code_files')
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    case_convert_file(path, CaseStyleEnum.CAMEL_CASE)
```

## Requirements

* > Anyone know a utility that can automatically change all identifiers’ case/underscore style for a whole file?  e.g. converting between FOO_BAR, fooBar, foo_bar, FooBar.

* You should not need to input the source file's case style. Case style should be auto-detected.

* It is allowed for input files to contain mixed case styles before transformation.

## License

MIT
