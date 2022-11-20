#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Gets user's name
    string name = get_string("What is your name?\n");

    // Prints out hello, users_name
    printf("hello, %s\n", name);
}