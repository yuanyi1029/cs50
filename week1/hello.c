#include <stdio.h>   // importing functions from standard.io library (io stands for input/output)
#include <cs50.h>    // importing functions from cs50 library (to use their precoded input functions)

int main(void)
{
    printf("hello, world\n");
    string answer = get_string("What's your name? ");    // get_string is a function from cs50 library
    printf("hello, %s! \n", answer);                    // %s: placeholder for a string
}