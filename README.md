# camelback

camelback is a Python utility to convert all identifiers in a source file between different casing styles.

Inspired by [this tweet.](https://twitter.com/comex/status/1062814338182868992)

The supported options for casing styles:

* `SNAKE_CASE`: `foo_bar`
* `MACRO_CASE`: `FOO_BAR`
* `CAMEL_CASE`: `fooBar`
* `PASCAL_CASE`: `FooBar`

## Example

```bash
$ cat code.c
```
```c
#include <stdio.h>  // printf
void foo_bar(int user_argument) {
    printf("%d\n", user_argument);
}
int main(int argc, char** argv) {
    int my_variable = 42;
    foo_bar(my_variable);
    return 0;
}
```
```bash
$ python3 CAMEL_CASE code.c code.h
Converted code.c to CAMEL_CASE.
Converted code.h to CAMEL_CASE.
$ cat code.c
```
```c 
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

## Requirements

* > Anyone know a utility that can automatically change all identifiers’ case/underscore style for a whole file?  e.g. converting between FOO_BAR, fooBar, foo_bar, FooBar.

* You should not need to input the source file's case style. Case style should be auto-detected.

* It is allowed for input files to contain mixed case styles before transformation.

## License

MIT
