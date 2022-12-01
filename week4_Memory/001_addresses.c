#include <stdio.h>

int main(void)
{
    int n = 50;
    // Pointer p is a variable that stores that address of integer variable n
    int *p = &n;
    char *s = "HI!";

    printf("%p\n", p);
    printf("%i\n", *p);

    // Optional to use &s to print address of s because by default, s stores the address of the first character of a string
    printf("%p\n", s);
    // Do not use *s to print the string, use %s for the placeholder instead (cannot use both %s and *s at the same time)
    printf("%s\n", s);
    // printf("%s\n", *s);      (This will cause an error)

    // Another method to print the address of characters (use &)
    printf("%p\n", &s[0]);
    printf("%p\n", &s[1]);
    printf("%p\n", &s[2]);
    printf("%p\n", &s[3]);

    // Method to print substrings (printf but starting from the address of s+1 or s+2)
    printf("%s\n", s);
    printf("%s\n", s+1);
    printf("%s\n", s+2);
}