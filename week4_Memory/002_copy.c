#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char *s = get_string("s: ");

    // If the string is too long, it will return NULL, so we create a validation to stop if its too long
    if (s == NULL)
    {
        return 1;
    }
    // Ask the computer for fixed size of memory with malloc()
    char *t = malloc(strlen(s) + 1);

    // If requested memory size is too large, it will return NULL, so we create a validation to stop if its too large
    if (t == NULL)
    {
        return 1;
    }

    for (int i = 0; i < strlen(s) + 1; i++)
    {
        t[i] = s[i];
    }

    // Convert first letter to uppercase
    t[0] = toupper(t[0]);

    printf("s: %s\n", s);
    printf("t: %s\n", t);

    // Always use free() after using malloc() to free up the space after done with it 
    free(t);

    return 0;
}