#include <stdio.h>  // printf

void fooBar(int userArgument) {
    printf("%d\n", userArgument);
}

int main(int argc, char** argv) {
    int myVariable = 42;
    fooBar(myVariable);
    return 0;
}
