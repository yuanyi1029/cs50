#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // Reallocating the size of arrays. Bad method because it relies on using realloc()
    // or for loops to copy the old array tot resize it
    // Initialise values in list
    int *list = malloc(3 * sizeof(int));
    if (list == NULL)
    {
        return 1;
    }

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    // ... Interesting code that uses up memory

    // Create a temporary list, using realloc() will copy the contents of list to temp automatically
    // Looping thorugh the list and copying to temp is not needed anymore with realloc()
    int *temp = realloc(list, 4 * sizeof(int));
    if (temp == NULL)
    {
        free(list);
        return 1;
    }

    list = temp;
    list[3] = 4;

    for (int i = 0; i < 4; i++)
    {
        printf("%i\n", list[i]);
    }

    free(list);
    return 0;
}