#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // s[3] will not cause an error and will print as 0 because the computer
    // stores an extra character of 0 at the end of a string to represent the
    // end of a string.
    // Note: Strings are just an array of chars
    string s = "HI!";
    printf("%i %i %i %i\n", s[0], s[1], s[2], s[3]);

    string words[2];
    words[0] = "HI!";
    words[1] = "BYE!";
    printf("%c%c%c\n", words[0][0], words[0][1], words[0][2]);
    printf("%c%C%C%C\n", words[1][0], words[1][1], words[1][2], words[1][3]);
}
