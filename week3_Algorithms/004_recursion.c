#include <cs50.h>
#include <stdio.h>

void draw(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw(height);
}

void draw(int n)
{
    // Basecase, start drawing when n is equal to 0 from n = 1 to n = n
    if (n <= 0)
    {
        return;
    }
    draw (n - 1);

    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("\n");
}