#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next_node;
}
node;

int main(int argc, char *argv[])
{
    // Reallocating the size of arrays. Good method because uses linked lists

    // Pointer that represents the start of the list
    node *list = NULL;

    // Loop through number of arguments given, assign the number to each argument
    for (int i = 1; i < argc; i++)
    {
        int number = atoi(argv[i]);

        // Create a node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            free(n)
            return 1;
        }

        // Populate the variables of a node
        n -> number = number;
        n -> next_node = NULL;

        // Make the newest node point to the previous node
        // n -> next_node = list because list was pointing to the previous node
        n -> next_node = list;

        // Make the list point to the newest node
        list = n;
    }

    // Make a pointer that points to the newest node
    node *pointer = list;

    // Repeat while the pointer is pointing to an actual valid node
    while (pointer != NULL)
    {
        printf("%i\n", pointer -> number);

        // Update the pointer to by going into itself and getting the address of next_node 
        pointer = pointer -> next_node;
    }

    pointer = list;
    while (pointer != NULL)
    {
        // Assign the after node, free the current node the jump to the after node
        node *next = pointer -> next_node;
        free(pointer);
        pointer = next;
    }
}