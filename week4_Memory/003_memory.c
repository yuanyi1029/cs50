#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // Array variables just store the address of the first element of the array
    // Size of array =  3 x the size of an integer (4)
    int *x = malloc(3 * sizeof(int));
    if (x == NULL)
    {
        return 1;
    }

    x[0] = 72;
    x[1] = 73;
    x[2] = 33;

    printf("%i\n", x[0]);
    printf("%i\n", x[1]);
    printf("%i\n", x[2]);

    printf("%p\n", &x[0]);
    printf("%p\n", &x[1]);
    printf("%p\n", &x[2]);

    free(x);

    return 0;
}