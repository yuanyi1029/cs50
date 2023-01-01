#include <stdio.h>
#include <cs50.h>

// Try running the code without these -> error because functions are declared below main function
// We copy the function header to the top to tell the compiler that the function exists, but below
int get_size(void);
void print_grid(int size);

int main(void)
{
    // Get size of grid
    int n = get_size();

    // Print grid of bricks
    print_grid(n);
}

int get_size(void)
{
    int n;
    do
    {
        n = get_int("Size: ");
    }
    while (n < 1);
    return n;
}

void print_grid(int size)
{
    for (int i=0;i<size;i++)
    {
        for (int j=0;j<size;j++)
        {
            printf("#");
        }
        printf("\n");
    }
}