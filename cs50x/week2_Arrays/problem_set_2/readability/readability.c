#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Gets input text
    string text = get_string("Text: ");

    // Counts letters, words and sentences with functions
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Determine letters per 100 words, sentences per 100 words, and grade
    float lettersper100words = (float) letters / words * 100;
    float sentencesper100words = (float) sentences / words * 100;
    float grade = 0.0588 * lettersper100words - 0.296 * sentencesper100words - 15.8;

    // Prints out grades depending on the ranges of score
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(grade));
    }
}

int count_letters(string text)
{
    int letters = 0;
    // Loop through each character, add 1 to letters if its an alphabet
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    // Loop through each character, add 1 to words if its a space
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    // Add another 1 to words because 2 words are between 1 space
    words++;
    return words;
}

int count_sentences(string text)
{
    // Loop through each character, add 1 to sentences if its a '.' or '!' or '?'
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

