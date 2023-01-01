// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include "dictionary.h"
// Self added
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hash_index = hash(word);

    node *cursor = table[hash_index];

    for (node *n = cursor; n != NULL; n = n -> next)
    {
        if (strcasecmp(n -> word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    // Hash function that gets the index of the first 2 characters of a word
    if (strlen(word) >= 2)
    {
        int hashvalue1 = toupper(word[0]) - 'A';
        int hashvalue2 = toupper(word[1]) - 'A';

        return (26 * hashvalue1) + hashvalue2;
    }
    else
    {
        int hashvalue1 = toupper(word[0]) - 'A';
        return 26 * hashvalue1;
    }
}

// Initialise a count variable to count the number of words for size() function
int word_count = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO

    // Open the file and represent it as a file pointer
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Error in opening the file");
        return false;
    }

    // word array for storing words (+1 because word have \0 at the end)
    char word_array[LENGTH + 1];

    // Loop through the strings from the file
    while (fscanf(file, "%s", word_array) != EOF)
    {
        word_count++;
        // Create node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Error in allocating a node");
            return 1;
        }

        // Assign the node with the word, set its next node to null
        strcpy(n -> word, word_array);
        n -> next = NULL;

        // Hash the word to get a hash value
        int hash_index = hash(word_array);

        // Insert node into hash table
        if (table[hash_index] == NULL)
        {
            // hash_index of hash table should point to the node if hash table is empty
            table[hash_index] = n;
        }
        else
        {
            // The node's next node should first point to where the hash table is pointing
            n -> next = table[hash_index];
            // Then assign the hash_index of hash table to point to the node
            table[hash_index] = n;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO

    // return the number of words in the dictionary
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    // Initialise a curose and temporary node
    node *cursor = NULL;
    node *temporary = NULL;

    // Loop through N times for the hash table
    for (int i = 0; i < N; i++)
    {
        // Start by pointing cursor to first node of the ith element in hash table
        cursor = table[i];

        // Loop until the end of the linked list
        while (cursor != NULL)
        {
            // Temporary node will point to the same node as cursor, cursor goes to next node to keep track, then free the temporary node
            temporary = cursor;
            cursor = cursor -> next;
            free(temporary);
        }
    }
    return true;
}
