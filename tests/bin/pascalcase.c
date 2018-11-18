#include <stdio.h>  // printf

void FooBar(int UserArgument) {
    printf("%d\n", UserArgument);
}

int main(int argc, char** argv) {
    int MyVariable = 42;
    FooBar(MyVariable);
    return 0;
}
