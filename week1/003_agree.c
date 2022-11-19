#include <cs50.h>
#include <stdio.h>

// Try inputing a string instead of char -> it gets rejected and it will prompt the user for input again
// This is cs50's library feature

int main(void)
{
    char c = get_char("Do you agree? ");

    // Must use Single Quotes for char, Double Quotes for string in C Programming
    if (c == 'y' || c == 'Y')                      
    {
        printf("Agreed.\n");
    }
    else if (c == 'n'|| c == 'N')
    {
        printf("Not Agreed.\n");
    }
}