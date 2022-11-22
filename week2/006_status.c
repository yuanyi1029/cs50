#include <cs50.h>
#include <stdio.h>

// If we run this code without any arguments, the error message pops up
// When we run 'echo $?' we get an integer 1. This is because we specifically chose to return 1,
// the exit status of a program is always 0 unless specified
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Missing command-line argument\n");
        return 1;
    }
    else
    {
        printf("hello, %s\n", argv[1]);
    }
}