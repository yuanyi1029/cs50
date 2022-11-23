#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


bool only_digits(string argument);
string encrypt_text(string text);
char rotate(char character, int key);


int main(int argc, string argv[])
{
    // Check for arguments unequal to 2 and if the second argument (key) consists of only digits
    if (argc != 2 || !only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        // Convert the key argument from string to int
        int key = atoi(argv[1]);

        // Get user plaintext input
        string plaintext = get_string("plaintext: ");

        // Loop through each character, call for rotate function to rotate all the characters and print it out
        printf("ciphertext: ");
        for (int i = 0; i < strlen(plaintext); i++)
        {
            char cipherchar = rotate(plaintext[i], key);
            printf("%c", cipherchar);
        }
        printf("\n");

    }
}

bool only_digits(string argument)
{
    // Loop through each character, if a character is not a digit, result will be false, return result
    bool result = true;
    for (int i = 0; i < strlen(argument); i++)
    {
        if (!(isdigit(argument[i])))
        {
            result = false;
        }
    }
    return result;
}

char rotate(char character, int key)
{
    // check for uppercase, lowercase, and other characters
    if (isupper(character))
    {
        // Convert ASCII character to alphabet index (A=0, B=1) by deducting the ASCII value of character with'A'
        // Use Caesar's algorithm to shift the characters
        // Convert the alphabet index back to ASCII character
        char return_char = (((character - 'A') + key) % 26) + 'A';
        return return_char;
    }
    else if (islower(character))
    {
        // Convert ASCII character to alphabet index (a=0, b=1) by deducting the ASCII value of character with 'a'
        // Use Caesar's algorithm to shift the characters
        // Convert the alphabet index back to ASCII character
        char return_char = (((character - 'a') + key) % 26) + 'a';
        return return_char;
    }
    else
    {
        // For other characters, return the original character (nothing happens)
        return character;
    }
}
