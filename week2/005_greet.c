#include <stdio.h>
#include <cs50.h>

// --- Command Line Arguments ---
// Arguments that we can add when running the code.
// We use 'int main(int argc, string argv[])' instead of 'int main(void)' to
// allow extra arguments, where argv is an array of strings while argc is the length of array.
// Run 'make greet' and then './greet yuanyi' will result in 'hello, yuanyi',
// where argv[0] is './greet' and argv[1] is 'yuanyi'
int main(int argc, string argv[])
{
    if (argc == 2)
    {
        printf("hello, %s\n", argv[1]);
    }
    else
    {
        printf("hello, world\n");
    }
}