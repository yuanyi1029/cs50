#include <stdio.h>

int main(void)
{
    // Original function of get_int and other input methods from cs50 library
    // Scanf function that gets user input and stores it at the address of x (&x)
    int x;
    printf("x: ");
    scanf("%i", &x);
    printf("x: %i\n", x);

    printf("---------------\n");

    char s[4];
    printf("s: ");
    scanf("%s", s);
    printf("s: %s\n", s);
}