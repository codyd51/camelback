#include <stdio.h>  // printf

void foo_bar(int user_argument) {
    printf("%d\n", user_argument);
}

int main(int argc, char** argv) {
    int my_variable = 42;
    foo_bar(my_variable);
    return 0;
}
