#include <stdio.h>  // printf

void FOO_BAR(int USER_ARGUMENT) {
    printf("%d\n", USER_ARGUMENT);
}

int main(int argc, char** argv) {
    int MY_VARIABLE = 42;
    FOO_BAR(MY_VARIABLE);
    return 0;
}
