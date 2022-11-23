#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_bricks(int height);


int main(void)
{
    // Get height of pyramid
    int height = get_height();

    // Print pyramid of bricks
    print_bricks(height);

}

// Function prompt and get user input
int get_height(void)
{
    // Gets an integer for height, loop back if not between 1 and 8 inclusive
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    return n;
}

// Function to print bricks of each row
void print_bricks(int height)
{
    // Loops through each row
    for (int i = 1; i <= height; i++)
    {
        // Loops through each character in a row, determines to print a hash or a space
        for (int j = 1; j <= height; j++)
        {
            if (j > height - i)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}