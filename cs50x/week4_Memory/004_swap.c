
#include <stdio.h>

void swap(int a, int b);
void swap2(int *a, int *b);

int main (void)
{
    // swap will not work but swap2 will. 
    // swap uses pass by value while swap2 goes to the address to change the value (pass by reference)
    int x = 1;
    int y = 2;

    printf("x is %i, y is %i\n", x, y);
    swap(x, y);
    printf("x is %i, y is %i\n", x, y);
    printf("---------------------------\n");
    printf("x is %i, y is %i\n", x, y);
    // Pass in the address of x and y
    swap2(&x, &y);
    printf("x is %i, y is %i\n", x, y);
}

void swap(int a, int b)
{
    // Always use a temporary variable when swapping to not lose a value
    int tmp = a;
    a = b;
    b = tmp;
}

void swap2(int *a, int *b)
{
    // Always use a temporary variable when swapping to not lose a value
    // Go to the addresses a and b and get the values and assign them accordingly
    int tmp = *a;
    *a = *b;
    *b = tmp;
}