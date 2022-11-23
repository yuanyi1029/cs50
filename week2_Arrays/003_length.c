#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    string name = get_string("What's your name? ");

    // check for each character of a string, if the character is not \0 (the last character),
    // then add 1 to the counter, if the character is equal to \0, break
    int n = 0;
    while (name[n] != '\0')
    {
        n++;
    }
    printf("%i\n", n);

    // Other method: Use strlen from string.h library
    int length = strlen(name);
    printf("%i\n", length);
}